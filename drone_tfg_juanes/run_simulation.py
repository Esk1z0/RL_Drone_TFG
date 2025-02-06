import os
import shutil
import time
from datetime import datetime

import gymnasium
import pandas as pd
import argparse

# Stable_Baselines3 y extensiones
from sb3_contrib import RecurrentPPO
from stable_baselines3.common.env_util import SubprocVecEnv
from stable_baselines3.common.vec_env import VecMonitor
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.logger import configure
from stable_baselines3.common.evaluation import evaluate_policy

# Wrappers propios
from enviroments_package import RemoveKeyObservationWrapper, ScaleRewardWrapper, ScaleActionWrapper, BinaryActionWrapper

# -------------------------------------------------------------------
# Datos y configuraciones generales
world_dir = "./simulation_package/worlds/my_frst_webots_world.wbt"
json_reward = "./configs/reward_package_config/motors_use.json"

model_dir = "./models/ppomodel"
log_dir = "./logs/"
data_collected_dir = "./data_collected/"

timesteps = 64#20480
n_steps = 64
batch_size = 64
lr = 1e-3
ent_coef = 0.06
num_envs = 1

# -------------------------------------------------------------------
# Funciones

def make_env():
    """Crea una función que retorne un init() para SubprocVecEnv,
       aplicando wrappers a tu entorno Drone-v1."""
    def _init():
        env = gymnasium.make(
            'drone_tfg_juanes/Drone-v1',
            simulation_path=world_dir,
            reward_json_path=json_reward,
            no_render=False
        )
        # Aplica los wrappers necesarios
        env = RemoveKeyObservationWrapper(env, remove_keys=["camera", "gps"])
        env = ScaleRewardWrapper(env, scale_factor=0.1)
        env = ScaleActionWrapper(env, in_low=-1, in_high=1, out_low=0, out_high=576)
        # Si quisieras acciones binarias:
        # env = BinaryActionWrapper(env, power_level=500)
        return env
    return _init


class TrainingCallback(BaseCallback):
    """Callback de entrenamiento para resetear y cerrar el entorno,
       evitando problemas de sincronización."""
    def __init__(self, env, verbose=1):
        super(TrainingCallback, self).__init__(verbose)
        self.env = env

    def _on_step(self) -> bool:
        return True

    def _on_rollout_start(self) -> None:
        self.env.reset()

    def _on_training_end(self):
        print("Entrenamiento finalizado. Cerrando el entorno...")
        self.env.close()


def move_and_rename_csv(src_dir, dst_dir, new_name):
    """
    Busca 'progress.csv' en 'src_dir' y lo copia/renombra a 'dst_dir/new_name'.
    """
    csv_file = 'progress.csv'
    src_path = os.path.join(src_dir, csv_file)

    if not os.path.exists(src_path):
        print("No se encontró el archivo 'progress.csv' en el directorio de origen.")
        return

    dst_path = os.path.join(dst_dir, new_name)
    shutil.copy2(src_path, dst_path)
    print(f"Archivo copiado y renombrado a {dst_path}")


def schedule_rate(initial_value, final_value, total_cycles, current_cycle):
    """
    Interpola linealmente entre 'initial_value' y 'final_value'
    según 'current_cycle / total_cycles'.
    """
    if current_cycle >= total_cycles:
        return final_value
    return initial_value + (final_value - initial_value) * (current_cycle / total_cycles)


def update_model(model, env, log_dir='./logs/', n_eval_episodes=10):
    """
    Evalúa el modelo y actualiza el archivo de evaluación en CSV si la recompensa es la mejor hasta el momento.
    Retorna True si mejora la recompensa máxima, False en caso contrario.
    """
    eval_file_path = os.path.join(log_dir, "evaluate.csv")

    # Asegurarse de que existe la carpeta y el archivo
    os.makedirs(log_dir, exist_ok=True)
    if not os.path.exists(eval_file_path):
        pd.DataFrame(columns=["reward", "timestamp"]).to_csv(eval_file_path, index=False)

    eval_df = pd.read_csv(eval_file_path)
    max_reward = eval_df["reward"].max() if not eval_df.empty else float('-inf')

    mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=n_eval_episodes, return_episode_rewards=False)

    if mean_reward > max_reward:
        new_row = pd.DataFrame({
            "reward": [mean_reward],
            "timestamp": [datetime.now().strftime("%Y%m%d_%H%M%S")]
        })
        new_row.to_csv(eval_file_path, mode='a', header=False, index=False)
        env.close()
        return True
    else:
        env.close()
        return False


def parse_args():
    parser = argparse.ArgumentParser(description="Script de entrenamiento con Stable Baselines3 y Webots.")

    # Opción para recibir la carpeta de guardado
    parser.add_argument(
        "--save-dir",
        type=str,
        default="./data",
        help="Directorio donde se guardarán los modelos, logs y otros archivos."
    )

    # Puedes añadir más argumentos si lo deseas...
    return parser.parse_args()


# -------------------------------------------------------------------
# Lógica principal
if __name__ == "__main__":
    # Primero parseamos los argumentos:
    args = parse_args()

    # Ajusta log_dir, data_collected_dir, model_dir con la ruta que pase el usuario
    base_save_dir = args.save_dir

    log_dir = os.path.join(base_save_dir, "logs")
    data_collected_dir = os.path.join(base_save_dir, "data_collected")
    model_dir = os.path.join(base_save_dir, "models", "ppomodel")

    # Asegura que las carpetas existen
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(data_collected_dir, exist_ok=True)
    os.makedirs(os.path.dirname(model_dir), exist_ok=True)


    # Crear el entorno vectorizado SubprocVecEnv con 'num_envs' copias
    env = SubprocVecEnv([make_env() for _ in range(num_envs)])
    env = VecMonitor(env)

    new_logger = configure(log_dir, ["stdout", "csv"])
    callback = TrainingCallback(env=env, verbose=1)

    if not os.path.exists(model_dir + ".zip"):
        print("first train")

        model = RecurrentPPO(
            "MultiInputLstmPolicy",
            env,
            verbose=1,
            n_steps=n_steps,
            batch_size=batch_size,
            learning_rate=lr,
            ent_coef=ent_coef
        )
        model.set_logger(new_logger)
        model.learn(total_timesteps=timesteps, callback=callback)
        model.save(model_dir)

        move_and_rename_csv(log_dir, data_collected_dir, f'ppo_data{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    else:
        print("retrainning")

        model = RecurrentPPO.load(model_dir + ".zip", env=env)
        model.set_logger(new_logger)
        model.learning_rate = lr
        model.ent_coef = ent_coef

        model.learn(total_timesteps=timesteps, callback=callback)
        time.sleep(5)
        move_and_rename_csv(log_dir, data_collected_dir, f'ppo_data{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

        # Evaluación del modelo en un entorno individual
        single_env = make_env()()
        if update_model(model, single_env, n_eval_episodes=10):
            model.save(path=model_dir)
    print("END TRAINNING")

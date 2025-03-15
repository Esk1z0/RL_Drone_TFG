import os
import shutil
import time
from datetime import datetime
import json

import gymnasium
import pandas as pd
import argparse

# Stable_Baselines3 y extensiones
from sb3_contrib import RecurrentPPO
from stable_baselines3.common.env_util import SubprocVecEnv
from stable_baselines3.common.vec_env import VecMonitor
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.callbacks import CallbackList
from stable_baselines3.common.logger import configure
from stable_baselines3.common.evaluation import evaluate_policy

# Wrappers propios
from enviroments_package import RemoveKeyObservationWrapper, ScaleRewardWrapper, ScaleActionWrapper, BinaryActionWrapper




# Datos y configuraciones generales ////////////////////////////////////////////////////////////////////////////////////

world_dir = "./simulation_package/worlds/my_frst_webots_world.wbt"
json_reward = "./configs/reward_package_config/motors_use.json"

model_dir = "./models/ppomodel"
log_dir = "./logs/"
data_collected_dir = "./data_collected/"

timesteps = 307200
n_steps = 1024
batch_size = 256
lr = 1e-3
ent_coef = 0.01
num_envs = 1




#Funciones  ////////////////////////////////////////////////////////////////////////////////////////////////////////////

def make_env():
    """Crea una función que retorne un init() para SubprocVecEnv,
       aplicando wrappers a tu entorno Drone-v1."""

    def _init():
        env = gymnasium.make(
            'drone_tfg_juanes/Drone-v1',
            simulation_path=world_dir,
            reward_json_path=json_reward,
            no_render=True
        )
        # Aplica los wrappers necesarios
        env = RemoveKeyObservationWrapper(env, remove_keys=["gps"])#["camera", "gps"])
        env = ScaleRewardWrapper(env, scale_factor=0.1)
        env = ScaleActionWrapper(env, in_low=-1, in_high=1, out_low=0, out_high=576)
        # Si quisieras acciones binarias:
        # env = BinaryActionWrapper(env, power_level=500)
        return env

    return _init

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




# callbacks ////////////////////////////////////////////////////////////////////////////////////////////////////////////

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


class CustomCheckpointCallback(BaseCallback):
    """
    Callback que guarda el modelo, logs y un checkpoint de entrenamiento después de cada rollout.
    - Guarda el modelo en "ruta_base/modelos/"
    - Guarda los logs en "ruta_base/logs/"
    - Guarda el número de timesteps entrenados en "ruta_base/checkpoint.json"
    """

    def __init__(self, log_dir, data_collected_dir, model_dir, verbose=1):
        """
        :param base_path: Ruta base donde se guardarán todos los archivos.
        :param model_prefix: Prefijo del modelo guardado.
        :param verbose: Nivel de detalle de impresión.
        """
        super().__init__(verbose)
        self.log_dir = log_dir
        self.data_collected_dir = data_collected_dir
        self.model_dir = model_dir

        # Archivo de checkpoint
        self.checkpoint_file = os.path.join(model_dir, "checkpoint.json")

        # Archivo de Datos
        self.data_collected_file = os.path.join(data_collected_dir, f'data_collected_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

    def _on_step(self) -> bool:
        return True

    def _on_rollout_start(self) -> None:
        """Se ejecuta al inicio de cada rollout (cuando se generan nuevos logs)."""
        self._save_checkpoint()

    def _on_training_end(self) -> None:
        """Se ejecuta al finalizar el entrenamiento para guardar el último estado."""
        self._save_checkpoint(final=True)

    def _save_checkpoint(self, final=False) -> None:
        """
        Guarda el modelo, copia/renombra el progress.csv y almacena un archivo JSON con los timesteps entrenados.
        """
        current_timesteps = self.model.num_timesteps
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Guardar modelo con un nombre que indica los timesteps entrenados
        model_name = "model_final.zip" if final else "model"
        model_path = os.path.join(self.model_dir, model_name)
        self.model.save(model_path)

        if self.verbose > 0:
            print(f"[SaveOnRolloutCallback] Modelo guardado en: {model_path}")

        # **Leer el valor anterior de los timesteps entrenados para sumarlos**
        previous_timesteps = 0
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, "r") as f:
                    checkpoint_data = json.load(f)
                    previous_timesteps = checkpoint_data.get("timesteps_trained", 0)  # Cargar los timesteps previos
            except Exception as e:
                print(f"[WARNING] No se pudo leer el JSON, reiniciando los timesteps: {e}")
                previous_timesteps = 0

        # **Sumar los nuevos timesteps al valor previo**
        total_timesteps = previous_timesteps + current_timesteps

        # Guardar checkpoint con el número de timesteps entrenados
        checkpoint_data = {
            "timesteps_trained": int(total_timesteps),
            "last_save_time": timestamp_str
        }
        with open(self.checkpoint_file, "w") as f:
            json.dump(checkpoint_data, f, indent=2)

        move_and_rename_csv(
            self.log_dir,
            self.data_collected_dir,
            self.data_collected_file
        )




# Lógica principal  ////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    # Parseamos el directorio base
    args = parse_args()
    base_save_dir = args.save_dir


    # Creamos las direcciones y las comprobamos
    log_dir = os.path.join(base_save_dir, "logs")
    data_collected_dir = os.path.join(base_save_dir, "data_collected")
    model_dir = os.path.join(base_save_dir, "models")

    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(data_collected_dir, exist_ok=True)
    os.makedirs(os.path.dirname(model_dir), exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    # cargar checkpoint
    checkpoint_file = os.path.join(model_dir, "checkpoint.json")

    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            checkpoint_data = json.load(f)
            trained_so_far = checkpoint_data.get("timesteps_trained", 0)
    else:
        trained_so_far = 0
        with open(checkpoint_file, "w") as f:
            json.dump({"timesteps_trained": trained_so_far}, f, indent=2)


    # Crear el entorno vectorizado SubprocVecEnv con 'num_envs' copias
    env = SubprocVecEnv([make_env() for _ in range(num_envs)])
    env = VecMonitor(env)

    new_logger = configure(log_dir, ["stdout", "csv"])

    trainning_callback = TrainingCallback(env=env, verbose=1)
    restart_callback = CustomCheckpointCallback(
        log_dir=log_dir,
        data_collected_dir=data_collected_dir,
        model_dir=model_dir
    )
    callbacks = CallbackList([trainning_callback, restart_callback])

    # Bucle de entrenamiento con reanudación automática
    while (timesteps - trained_so_far) > 0:
        try:
            # Cargar modelo si existe, sino iniciar nuevo
            model_path = os.path.join(model_dir, f"model.zip")
            if os.path.exists(model_path):
                print(f"[INFO] Cargando modelo desde {model_path}")
                model = RecurrentPPO.load(model_path, env=env)
            else:
                print("[INFO] No se encontró un modelo previo. Creando uno nuevo...")
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


            # Entrenar el Modelo
            print(f"[INFO] Timesteps restantes: {timesteps - trained_so_far}")
            train_steps = timesteps - trained_so_far # Entrena en bloques
            model.learn(total_timesteps=train_steps, reset_num_timesteps=False, callback=callbacks)

            move_and_rename_csv(log_dir, data_collected_dir, f'ppo_data{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
            model.save(path=os.path.join(model_dir, "model_final"))

            trained_so_far = timesteps

        except Exception as e:
            print(f"[ERROR] Se produjo un error durante el entrenamiento: {e}")
            time.sleep(5)  # Espera unos segundos antes de reintentar

            #if env is not None: env.close()
            env = None

            # Crear el entorno vectorizado SubprocVecEnv con 'num_envs' copias
            env = SubprocVecEnv([make_env() for _ in range(num_envs)])
            env = VecMonitor(env)

            new_logger = configure(log_dir, ["stdout", "csv"])

            trainning_callback = TrainingCallback(env=env, verbose=1)
            restart_callback = CustomCheckpointCallback(
                log_dir=log_dir,
                data_collected_dir=data_collected_dir,
                model_dir=model_dir
            )
            callbacks = CallbackList([trainning_callback, restart_callback])

            #cogemos el json
            with open(checkpoint_file, "r") as f:
                checkpoint_data = json.load(f)
                trained_so_far = checkpoint_data.get("timesteps_trained", 0)

    print("[INFO] Entrenamiento finalizado.")

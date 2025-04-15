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

from stable_baselines3.common.callbacks import CallbackList
from stable_baselines3.common.logger import configure
from stable_baselines3.common.evaluation import evaluate_policy

# Wrappers propios
from environments_package import RemoveKeyObservationWrapper, ScaleRewardWrapper, ScaleActionWrapper
# Callbacks propios
from environments_package import CustomCheckpointCallback, TrainingCallback




# Datos y configuraciones generales ////////////////////////////////////////////////////////////////////////////////////

world_dir = "./simulation_package/worlds/bioloid_env.wbt"
json_reward = "./configs/reward_package_config/test_bioloid.json"

model_dir = "./models/ppomodel"
log_dir = "./logs/"
data_collected_dir = "./data_collected/"

timesteps = 1024#307200
n_steps = 64#1024
batch_size = 16#256
lr = 1e-3
ent_coef = 0.01
num_envs = 1




#Funciones  ////////////////////////////////////////////////////////////////////////////////////////////////////////////

def make_env():
    """Crea una función que retorne un init() para SubprocVecEnv,
       aplicando wrappers a tu entorno Drone-v1."""

    def _init():
        env = gymnasium.make(
            'tfg_juanes/CustomBioloid-v1',
            simulation_path=world_dir,
            reward_json_path=json_reward,
            no_render=False
        )
        # Aplica los wrappers necesarios
        env = RemoveKeyObservationWrapper(env, remove_keys=["gps"])#["camera", "gps"])
        env = ScaleRewardWrapper(env, scale_factor=1.5)
        env = ScaleActionWrapper(env)
        return env

    return _init





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
    model_path = os.path.join(model_dir, "model.zip")

    if os.path.exists(checkpoint_file) and os.path.exists(model_path):
        with open(checkpoint_file, "r") as f:
            checkpoint_data = json.load(f)
            trained_so_far = checkpoint_data.get("timesteps_trained", 0)
        print(f"[INFO] Checkpoint encontrado. Timesteps entrenados hasta ahora: {trained_so_far}")
    else:
        trained_so_far = 0
        with open(checkpoint_file, "w") as f:
            json.dump({"timesteps_trained": trained_so_far}, f, indent=2)
        print("[INFO] No se encontró modelo o checkpoint. Entrenamiento comenzará desde cero.")

    # Crear el entorno vectorizado SubprocVecEnv con 'num_envs' copias
    env = SubprocVecEnv([make_env() for _ in range(num_envs)], start_method='spawn')
    env = VecMonitor(env)

    new_logger = configure(log_dir, ["stdout", "csv"])

    trainning_callback = TrainingCallback(env=env, verbose=1)
    restart_callback = CustomCheckpointCallback(
        log_dir=log_dir,
        data_collected_dir=data_collected_dir,
        model_dir=model_dir,
        n_steps=n_steps,
        last_checkpoint=trained_so_far
    )
    callbacks = CallbackList([trainning_callback, restart_callback])

    # Entrenar solo si quedan timesteps
    if (timesteps - trained_so_far) > 0:
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
        print(f"[INFO] Timesteps restantes: {timesteps - trained_so_far}")

        train_steps = timesteps - trained_so_far
        model.learn(total_timesteps=train_steps, reset_num_timesteps=False, callback=callbacks)


    print("[INFO] Entrenamiento finalizado.")

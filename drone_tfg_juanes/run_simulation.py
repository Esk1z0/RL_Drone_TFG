import os
import json
import argparse

import gymnasium
import torch
from sb3_contrib import RecurrentPPO
from stable_baselines3.common.env_util import SubprocVecEnv
from stable_baselines3.common.vec_env import VecMonitor
from stable_baselines3.common.callbacks import CallbackList
from stable_baselines3.common.logger import configure

from environments_package import (
    RemoveKeyObservationWrapper,
    ScaleRewardWrapper,
    ScaleActionWrapper,
    CustomCheckpointCallback,
    TrainingCallback
)

# Configuraciones generales
WORLD_PATH = "./simulation_package/worlds/bioloid_env.wbt"
REWARD_CONFIG_PATH = "./configs/reward_package_config/test_bioloid.json"
DEFAULT_SAVE_DIR = "./data"
DEFAULT_TIMESTEPS = 307200
DEFAULT_N_STEPS = 1024
DEFAULT_BATCH_SIZE = 256
DEFAULT_LR = 1e-3
DEFAULT_ENT_COEF = 0.01
NUM_ENVS = 1


def make_env():
    """Crea y devuelve una función de inicialización del entorno."""
    def _init():
        env = gymnasium.make(
            'tfg_juanes/CustomBioloid-v1',
            simulation_path=WORLD_PATH,
            reward_json_path=REWARD_CONFIG_PATH,
            no_render=False
        )
        env = RemoveKeyObservationWrapper(env, remove_keys=["gps"])
        env = ScaleRewardWrapper(env, scale_factor=1.5)
        env = ScaleActionWrapper(env)
        return env

    return _init


def parse_args():
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description="Entrenamiento con SB3 y Webots.")
    parser.add_argument(
        "--save-dir",
        type=str,
        default=DEFAULT_SAVE_DIR,
        help="Directorio para guardar modelos y logs."
    )
    return parser.parse_args()


def prepare_directories(base_dir):
    """Crea las carpetas necesarias si no existen."""
    log = os.path.join(base_dir, "logs")
    data = os.path.join(base_dir, "data_collected")
    model = os.path.join(base_dir, "models")
    os.makedirs(log, exist_ok=True)
    os.makedirs(data, exist_ok=True)
    os.makedirs(model, exist_ok=True)
    return log, data, model


def load_checkpoint(model_dir):
    """Carga información del checkpoint si existe."""
    checkpoint_path = os.path.join(model_dir, "checkpoint.json")
    model_path = os.path.join(model_dir, "model.zip")

    if os.path.exists(checkpoint_path) and os.path.exists(model_path):
        with open(checkpoint_path, "r") as f:
            data = json.load(f)
        print(f"[INFO] Checkpoint encontrado. Timesteps entrenados: {data.get('timesteps_trained', 0)}")
        return data.get("timesteps_trained", 0), model_path

    with open(checkpoint_path, "w") as f:
        json.dump({"timesteps_trained": 0}, f, indent=2)
    print("[INFO] No se encontró modelo. Entrenamiento desde cero.")
    return 0, model_path


def main():
    print(f"[INFO] Dispositivo: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

    args = parse_args()
    log_dir, data_dir, model_dir = prepare_directories(args.save_dir)
    trained_so_far, model_path = load_checkpoint(model_dir)

    env = SubprocVecEnv([make_env() for _ in range(NUM_ENVS)], start_method='spawn')
    env = VecMonitor(env)
    logger = configure(log_dir, ["stdout", "csv"])

    callbacks = CallbackList([
        TrainingCallback(env=env, verbose=1),
        CustomCheckpointCallback(
            log_dir=log_dir,
            data_collected_dir=data_dir,
            model_dir=model_dir,
            n_steps=DEFAULT_N_STEPS,
            last_checkpoint=trained_so_far
        )
    ])

    remaining_steps = DEFAULT_TIMESTEPS - trained_so_far

    if remaining_steps > 0:
        if os.path.exists(model_path):
            print(f"[INFO] Cargando modelo desde {model_path}")
            model = RecurrentPPO.load(model_path, env=env)
        else:
            print("[INFO] Creando nuevo modelo...")
            model = RecurrentPPO(
                "MultiInputLstmPolicy",
                env,
                verbose=1,
                n_steps=DEFAULT_N_STEPS,
                batch_size=DEFAULT_BATCH_SIZE,
                learning_rate=DEFAULT_LR,
                ent_coef=DEFAULT_ENT_COEF
            )

        model.set_logger(logger)
        print(f"[INFO] Timesteps por entrenar: {remaining_steps}")
        model.learn(total_timesteps=remaining_steps, reset_num_timesteps=False, callback=callbacks)

    print("[INFO] Entrenamiento finalizado.")


if __name__ == "__main__":
    main()

import json
import os
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

from configs.trainning_config_loader import TrainingConfigLoader


def make_env(world_path, reward_json_path, no_render):
    def _init():
        env = gymnasium.make(
            'tfg_juanes/CustomBioloid-v1',
            simulation_path=world_path,
            reward_json_path=reward_json_path,
            no_render=no_render
        )
        env = RemoveKeyObservationWrapper(env, remove_keys=["gps"])
        env = ScaleRewardWrapper(env, scale_factor=1.5)
        env = ScaleActionWrapper(env)
        return env
    return _init


def parse_args():
    parser = argparse.ArgumentParser(description="Entrenamiento con SB3 y Webots.")
    parser.add_argument(
        "--save-dir",
        type=str,
        default=".",
        help="Directorio para guardar modelos y logs."
    )
    return parser.parse_args()


def prepare_directories(base_dir):
    log = os.path.join(base_dir, "logs")
    data = os.path.join(base_dir, "data_collected")
    model = os.path.join(base_dir, "models")
    os.makedirs(log, exist_ok=True)
    os.makedirs(data, exist_ok=True)
    os.makedirs(model, exist_ok=True)
    return log, data, model


def load_checkpoint(model_dir):
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
    config_loader = TrainingConfigLoader(os.path.join(args.save_dir, "config.json"))
    config = config_loader.load()

    log_dir, data_dir, model_dir = prepare_directories(args.save_dir)
    trained_so_far, model_path = load_checkpoint(model_dir)

    env = SubprocVecEnv([
        make_env(
            config.env_config.get("world_path"),
            os.path.join(args.save_dir, config.env_config.get("reward_json_path")),
            config.env_config.get("no_render", False)
        ) for _ in range(config.train_config.get("num_envs", 1))
    ], start_method='spawn')
    env = VecMonitor(env)
    logger = configure(log_dir, ["stdout", "csv"])

    callbacks = CallbackList([
        TrainingCallback(env=env, verbose=1),
        CustomCheckpointCallback(
            log_dir=log_dir,
            data_collected_dir=data_dir,
            model_dir=model_dir,
            n_steps=config.model_config.get("params", {}).get("n_steps", 2048),
            last_checkpoint=trained_so_far
        )
    ])

    remaining_steps = config.train_config.get("timesteps", 100000) - trained_so_far

    model_class = globals().get(config.model_config.get("algorithm"))
    if model_class is None:
        raise ValueError(f"Algoritmo desconocido: {config.model_config.get('algorithm')}")

    if remaining_steps > 0:
        if os.path.exists(model_path):
            print(f"[INFO] Cargando modelo desde {model_path}")
            model = model_class.load(model_path, env=env)
        else:
            print("[INFO] Creando nuevo modelo...")
            model = model_class(
                config.model_config.get("policy"),
                env,
                verbose=1,
                **config.model_config.get("params", {})
            )

        model.set_logger(logger)
        print(f"[INFO] Timesteps por entrenar: {remaining_steps}")
        model.learn(total_timesteps=remaining_steps, reset_num_timesteps=False, callback=callbacks)

    print("[INFO] Entrenamiento finalizado.")


if __name__ == "__main__":
    main()

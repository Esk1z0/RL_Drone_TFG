import os
import argparse

import gymnasium
import torch
from stable_baselines3.common.env_util import SubprocVecEnv
from stable_baselines3.common.vec_env import VecMonitor

from environments_package import RemoveKeyObservationWrapper, ScaleActionWrapper
from configs.trainning_config_loader import TrainingConfigLoader
from models_package.algorithm_factory import RLModelFactory


def parse_args():
    """Parsea los argumentos de línea de comandos para determinar la ruta base de guardado."""
    parser = argparse.ArgumentParser(description="Entrenamiento con SB3 y Webots.")
    parser.add_argument(
        "--save-dir",
        type=str,
        default=".",
        help="Directorio para guardar modelos y logs."
    )
    return parser.parse_args()


def make_env(world_path, reward_json_path, no_render):
    """Devuelve una función de inicialización del entorno, con todos los wrappers aplicados."""
    def _init():
        env = gymnasium.make(
            'tfg_juanes/CustomBioloid-v1',
            simulation_path=world_path,
            reward_json_path=reward_json_path,
            no_render=no_render
        )
        # Aplicamos los wrappers necesarios al entorno
        env = RemoveKeyObservationWrapper(env, remove_keys=["gps"])
        env = ScaleActionWrapper(env)
        return env
    return _init


def create_env(config, save_dir):
    """Crea un entorno vectorizado VecMonitor con múltiples entornos en paralelo."""
    env = SubprocVecEnv([
        make_env(
            config.env_config.get("world_path"),
            os.path.join(save_dir, config.env_config.get("reward_json_path")),
            config.env_config.get("no_render", False)
        ) for _ in range(config.train_config.get("num_envs", 1))
    ], start_method='spawn')
    return VecMonitor(env)


def main():
    """Función principal que organiza el proceso de entrenamiento del agente"""
    print(f"[INFO] Dispositivo: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

    # Cargamos los argumentos y el archivo de configuración
    save_dir = parse_args().save_dir
    config = TrainingConfigLoader(os.path.join(save_dir, "config.json")).load()

    # Creamos el entorno y el modelo
    env = create_env(config, save_dir)
    model_factory = RLModelFactory(config, env, save_dir)

    # Calculamos los pasos restantes por entrenar y entrenamos si aún quedan
    remaining_steps = config.train_config.get("timesteps") - model_factory.get_trained_steps()
    if remaining_steps > 0:
        model, callbacks = model_factory.create_or_load_model()
        print(f"[INFO] Timesteps por entrenar: {remaining_steps}")
        model.learn(total_timesteps=remaining_steps, reset_num_timesteps=False, callback=callbacks)

    print("[INFO] Entrenamiento finalizado.")


if __name__ == "__main__":
    main()
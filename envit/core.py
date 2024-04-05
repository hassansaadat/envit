import os
from decouple import Config, RepositoryEnv

config = None


def load_env_variables():
    global config  # Use global keyword to modify the module-level variable
    default_env_dir = os.getenv('DEFAULT_ENV_DIR', 'envs')
    environment = os.getenv('ENVIRONMENT')
    if not environment:
        print("Error: Environment variable ENVIRONMENT must be set.")
        return

    env_file_path = os.path.join(default_env_dir, f'{environment}.env')
    if not os.path.isfile(env_file_path):
        print(f"Error: Environment file '{env_file_path}' not found.")
        return

    config = Config(RepositoryEnv(env_file_path))


__all__ = ['config']


load_env_variables()

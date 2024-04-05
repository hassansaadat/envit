import os
import tempfile
import pytest


@pytest.fixture(scope='module')
def setup_env():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    # Create a 'envs' directory within the temporary directory
    envs_dir = os.path.join(temp_dir, 'envs')
    os.makedirs(envs_dir)
    # Create a 'production.env' file with some configurations
    production_file_content = """
        DB_HOST=localhost\n
        DB_PORT=5432\n
        DB_USER=admin\n
        DB_PASSWORD=password\n
    """
    with open(os.path.join(envs_dir, 'production.env'), 'w') as f:
        f.write(production_file_content)

    os.environ['DEFAULT_ENV_DIR'] = envs_dir
    os.environ['ENVIRONMENT'] = 'production'

    yield

    # Teardown: Remove the temporary directory and its contents
    import shutil
    shutil.rmtree(temp_dir)


def test_environment_variables(setup_env):
    from envit.core import config

    # Test that environment variables are loaded correctly
    assert config('DB_HOST') == 'localhost'
    assert config('DB_PORT', cast=int) == 5432
    assert config('DB_USER') == 'admin'
    assert config('DB_PASSWORD') == 'password'

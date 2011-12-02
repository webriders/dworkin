import os
from fabric.api import local, lcd


VIRTUAL_ENV_DIR = 'virtualenv'
PROJECT_NAME = 'dworkin'

def get_virtual_env_bin(command):
    path = os.path.join(VIRTUAL_ENV_DIR, PROJECT_NAME, 'bin')
    if command:
        path = os.path.join(path, command)
    return path

def create_virtualenv():
    if not os.path.isdir(VIRTUAL_ENV_DIR):
        os.mkdir(VIRTUAL_ENV_DIR)
    with lcd(VIRTUAL_ENV_DIR):
        local('virtualenv --distribute ' + PROJECT_NAME)
    local(get_virtual_env_bin('pip') + ' install -r requirements.txt')
    local(get_virtual_env_bin('pip') + ' install -r requirements_dev.txt')

def run_tests():
    with lcd('source'):
        local('../' + get_virtual_env_bin('python') + ' manage.py jenkins')

def jenkins():
    create_virtualenv()
    run_tests()


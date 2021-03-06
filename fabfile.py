# coding: utf-8
from fabric.api import run, env, cd, prefix, shell_env, local
from config import load_config

config = load_config()
host_string = config.HOST_STRING


def deploy():
    env.host_string = config.HOST_STRING
    run('sudo chmod 777 -R /var/www/sneakerbox')
    print('chmod in /var/www/sneakerbox changet to 777')
    with cd('/var/www/sneakerbox'):
        with shell_env(MODE='PRODUCTION'):
            run('git reset --hard HEAD')
            run('git pull')
            run('npm install')
            run('gulp')
            with prefix('source venv/bin/activate'):
                run('pip install -r requirements.txt')
                run('python manage.py db upgrade')
                run('python manage.py build')
            run('supervisorctl restart sneakerbox')
            run('sudo chmod 654 -R /var/www/sneakerbox')
            print('chmod in /var/www/sneakerbox changet to 654')


def restart():
    env.host_string = config.HOST_STRING
    run('sudo supervisorctl restart sneakerbox')

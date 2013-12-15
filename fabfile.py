from fabric.api import env, run, sudo, cd, local
from ydcommon.fab import *

env.hosts = ['amazon-dev', ]
env.use_ssh_config = True
dev_on_sh = True


def get_vars(keys):
    branch = local("git branch --no-color 2> /dev/null | sed -e '/^[^*]/d'", capture=True).replace("* ", "").strip()
    user = 'ubuntu'
    prefix = "dev"
    environment = 'sew'
    app_dir = 'public_html/sew_django'
    if branch == 'develop' and dev_on_sh:
        env.host_string = 'am.ivolution.pl'
        env.user = "ubuntu"
        user = "sew"
        environment = "sew"

    data = {
        'user': user,
        'path': '/home/%s/%s/' % (user,app_dir),
        'python': '/home/%s/Envs/%s/bin/python' % (user, environment),
        'pip': '/home/%s/Envs/%s/bin/pip' % (user, environment),
        'prefix': prefix,
        'environment': environment,
        'app_dir': app_dir,
    }
    return [data.get(k) for k in keys]


def deploy(full=False, libs=False, migrate=False):
    """
        Deploy new code
    """
    user, path, python, pip, prefix, app_dir, environment = get_vars(['user', 'path', 'python', 'pip', 'prefix', 'app_dir', 'environment'])
    with cd(path):
        sudo('git pull', user=user)
        check_branch(environment, user=user)
        sudo('find . -name "*.pyc" -delete', user=user)
        if full or libs:
            sudo(pip + ' install -r requirements.txt', user=user)
            sudo('npm install', user=user)
            sudo('find /home/%s/Envs/%s/ -name "*.pyc" -delete' % (user, environment), user=user)
        if full or migrate:
            sudo(python + ' manage.py syncdb', user=user)
            sudo(python + ' manage.py migrate', user=user)
        sudo(python + ' manage.py collectstatic -v0 --noinput', user=user)
        sudo(python + ' manage.py compress -f', user=user)

    if environment == 'production':
        output = run('ps ax|grep %s-%s.fcgi' % (user, prefix), shell=False)
        for line in output.split("\n"):
            if line.find('grep') == -1:
                pid = line.strip().split(' ')[0]
        sudo('kill -9 %s' % pid)
        output = run('ps ax|grep %s-%sl.fcgi' % (user, prefix), shell=False)
        for line in output.split("\n"):
            if line.find('grep') == -1:
                pid = line.strip().split(' ')[0]
        sudo('kill -9 %s' % pid)
        for line in output.split("\n"):
            if line.find('grep') == -1:
                pid = line.strip().split(' ')[0]
        sudo('kill -9 %s' % pid)
    else:
        sudo('supervisorctl restart sew')
    #if full:
    #    update_cron()


def command(command):
    """
        Run custom Django management command
    """
    user, path, python = get_vars(['user', 'path', 'python'])
    with cd(path):
        sudo(python + ' manage.py %s' % command, user=user)


def update_cron():
    """
        Update cron
    """
    user, path, environment = get_vars(['user', 'path', 'environment'])
    cdir = 'prod' if environment == 'production' else environment
    sudo('crontab  %sconfig/%s/crontab' % (path, cdir), user=user)

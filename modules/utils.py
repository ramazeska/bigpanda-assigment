import os
import subprocess as sub
import json
import shutil
import shlex


class RunCmd:
    def run_cmd(self, cmd: str):
        if cmd is not None:
            proc = sub.Popen(shlex.split(cmd), stderr=sub.PIPE, stdout=sub.PIPE, universal_newlines=True)
            stdout , stderr = proc.communicate()
            if proc.returncode != 0:
                print('stdout: {}\nstderr: {}'.format(stdout, stderr))
                raise Exception('{} exited with retruncode: {}'.format(cmd, proc.returncode))
            return 'stdout: {}\nstderr: {}'.format(stdout, stderr)

    def get_cmd_path(self, cmd: str):
        return shutil.which(cmd)


class initDefaults(RunCmd):
    def __init__(self):
        RunCmd.__init__(self)
        curr_location = os.path.dirname(__file__)
        app_root = os.path.dirname(curr_location)
        self.configs_path = os.path.join(app_root, 'configs')
        self.config = json.loads(open(os.path.join(self.configs_path, 'config.json')).read())
        self.docker = self._check_if_docker_installed()
        self.git = self._check_if_git_installed()
        self.compose = self._check_if_docker_compose_installed() # docker-compose app
        self.image_path = self._create_image_path()
        self.compose_path = os.path.join(app_root, 'compose')
        self.config['compose_file'] = os.path.join(self.configs_path, 'docker-compose.yml')
        if os.path.exists(self.config['tmpzip']):
            os.unlink(self.config['tmpzip'])
        if os.path.exists(self.compose_path):
            shutil.rmtree(self.compose_path)

    def copy(self, src: str, dst: str):
        return shutil.copy(src, dst)

    def _create_image_path(self):
        if not os.path.exists(self.config['image_path']):
            os.mkdir(self.config['image_path'])
            return self.config['image_path']

        if os.path.isdir(self.config['image_path']):
            for r,s,f in os.walk(self.config['image_path']):
                for ff in f:
                    os.unlink(os.path.join(r,ff))

            return self.config['image_path']

        if os.path.exists(self.config['image_path']) and not os.path.isdir(self.config['image_path']):
            raise Exception('{} allready exists and its not a directory'.format(self.config('image_path')))

    def _check_validator(self, cmd: str, inp):
        if type(inp) is str:
            return inp
        raise Exception('{} not in path or not installed'.format(cmd))

    def _check_if_docker_compose_installed(self):
        compose = self.get_cmd_path('docker-compose')
        return self._check_validator(cmd='docker-compose', inp=compose)

    def _check_if_docker_installed(self):
        docker = self.get_cmd_path('docker')
        return self._check_validator(cmd='docker', inp=docker)

    def _check_if_git_installed(self):
        git = self.get_cmd_path('git')
        return self._check_validator(cmd='git', inp=git)




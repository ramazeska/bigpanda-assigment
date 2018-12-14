from utils import initDefaults
import urllib.request
import tarfile
import ssl
import os

def get_images(url, tgt):

    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        images = urllib.request.urlretrieve(url, tgt)
        return True
    except Exception as e:
        raise e


def main():
    print('Init Settings')
    defaults = initDefaults()
    print('Done')
    try:
        print('Downloading and extracting archive')
        if get_images(defaults.config['image_resources'], defaults.config['tmpzip']) is True:
            tf = tarfile.open(defaults.config['tmpzip'])
            tf.extractall(path=defaults.config['image_path'])
        print('Done')

        clone_cmd = '{} clone {} {}/ops-exercise'.format(defaults.git, defaults.config['app_git'], defaults.compose_path)
        print(defaults.run_cmd(clone_cmd))

        print('modify apps dockerfile to run healthcheck')
        dokcerfile_path = os.path.join(defaults.compose_path, 'ops-exercise', 'Dockerfile')
        src_dockerfile = open(dokcerfile_path).readlines()
        src_dockerfile.insert(1, 'RUN apk update && apk add --no-cache curl')
        with open(dokcerfile_path, 'w') as tgt:
            tgt.write('\n'.join(src_dockerfile))

        print('Done')


        print('Create .env for docker-compose')
        with open('{}/.env'.format(defaults.compose_path), 'w') as compose_env:
            compose_env.write('IMAGES_PATH={}'.format(defaults.config['image_path']))
            compose_env.close()
        print('Done')
        print('copy compose default file to compose dir')
        defaults.copy(defaults.config['compose_file'], defaults.compose_path)
        print('Done')
        print('run the compose build and start')
        os.chdir(defaults.compose_path)
        docker_build_cmd = "{} build --no-cache --force-rm".format(defaults.compose)
        print(defaults.run_cmd(docker_build_cmd))
        print(defaults.run_cmd('{} up -d'.format(defaults.compose)))

    except Exception as e:
        raise e




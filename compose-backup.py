#!/usr/bin/env python3

import sys
import argparse
import yaml
import docker
import logging


docker_image = "compose-backuper"
docker_src_mount = '/mnt/src'
docker_dst_mount = '/mnt/dst'


def create_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('compose-backup')
    logger.setLevel(logging.INFO)
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    return logger


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--compose-file", type=str, default="./docker-compose.yml",
                        help="output path for backups", action="store")
    parser.add_argument("-p", "--output-path", type=str, default='.',
                        help="output path for backups", action="store")
    return vars(parser.parse_args())


def get_volume_parameters(context):
    if context.find(':'):
        if len(context.split(':')) == 3:
            volume, docker_mntpoint, mode = context.split(':')
        elif len(context.split(':')) == 2:
            volume, docker_mntpoint = context.split(':')
            mode = ""
    else:
        volume = context
        docker_mntpoint, mode = "", ""

    return volume, docker_mntpoint, mode


def volume_is_named(volume):
    docker_cli = docker.from_env()
    try:
        docker_cli.volumes.get(volume)
        return True
    except docker.errors.NotFound:
        logger.info('Volume {} is not a named volume, skipping.'.format(volume))
        return False


def get_host_mntpoint(volume):
    docker_cli = docker.from_env()
    volume_obj = docker_cli.volumes.get(volume)
    return volume_obj.attrs['Mountpoint']


def get_volumes_from_compose(compose_file):
    """
    Returns dict of services with volumes.
    Example:
    {'jenkins-nginx': [],
     'jenkins-master': [{'volume_id': 'jenkins-data',
                         'docker_mntpoint': '/var/jenkins_home'}]}
    """
    try:
        with open(compose_file) as stream:
            compose_content = yaml.load(stream)
    except IOError:
        print('Cannot find docker-compose.yml here!\nTry with -f option')
        sys.exit(1)

    services = [service for service in compose_content['services']]

    volumes_total_info = {}

    for service in services:

        volume_contexts = compose_content['services'][service]['volumes']
        volume_info = []

        for context in volume_contexts:

            volume, docker_mntpoint, mode = get_volume_parameters(context)
            logger.info(volume, docker_mntpoint, mode)

            if volume_is_named(volume):
                volume_info.append({'volume_id': volume,
                                    'docker_mntpoint': docker_mntpoint})

        volumes_total_info[service] = volume_info

    return volumes_total_info


def backup_volume(service_name, volume_id, output_path):
    docker_cli = docker.from_env()
    logger.info("Saving {}[{}]...".format(service_name, volume_id))
    docker_cli.containers.run(docker_image,
                              command='{}_{}'.format(service_name, volume_id),
                              volumes={volume_id: {'bind': docker_src_mount,
                                                   'mode': 'ro'},
                                       output_path: {'bind': docker_dst_mount,
                                                     'mode': 'rw'}})
    logger.info("Saved {}[{}].".format(service_name, volume_id))


if __name__ == '__main__':

    logger = create_logger()

    options = parse_args(sys.argv)
    volumes_info = get_volumes_from_compose(options['compose_file'])

    for service in volumes_info:
        for volume in volumes_info[service]:

            backup_volume(service_name=service,
                          volume_id=volume['volume_id'],
                          output_path=options['output_path'])

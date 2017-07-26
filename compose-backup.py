#!/usr/bin/env python3

import os
import sys
import argparse
import yaml
import docker
import logging

runner_image = "approximatenumber/compose-backuper"
runner_name = "compose-backuper"
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
                        help="path to docker-compose.yml", action="store")
    cwd = os.getcwd()
    parser.add_argument("-p", "--project-name", type=str, default=cwd,
                        help="project name", action="store")
    parser.add_argument("-d", "--destination", type=str, default='.',
                        help="destination directory for backups", action="store")
    return vars(parser.parse_args())


def open_compose_file(compose_file):
    try:
        with open(compose_file) as stream:
            return yaml.load(stream)
    except IOError:
        logger.error('Cannot find docker-compose.yml here! Try with -f option')
        sys.exit(1)


def get_volumes(compose_content):

    docker_cli = docker.from_env()

    project_name = options['project_name']

    compose_volumes = [vol for vol in compose_content['volumes']]

    volumes = []

    for vol_id in compose_volumes:

        try:
            # volume driver is local
            vol = docker_cli.volumes.get("{}_{}".format(project_name, vol_id))
            volumes.append(vol.attrs['Name'])

        except docker.errors.NotFound:
            try:
                # volume is external
                vol = docker_cli.volumes.get(vol_id)
                volumes.append(vol.attrs['Name'])

            except docker.errors.NotFound:
                logger.info('Cannot find volume %s!' % vol_id)

    return volumes


def backup_volume(volume_id, destination):

    docker_cli = docker.from_env()
    logger.info("{}: saving...".format(volume_id))
    docker_cli.containers.run(runner_image,
                              command='{}'.format(volume_id),
                              volumes={volume_id: {'bind': docker_src_mount,
                                                   'mode': 'ro'},
                                       destination: {'bind': docker_dst_mount,
                                                     'mode': 'rw'}},
                              remove=True,
                              name=runner_name
                              )
    logger.info("{}: saved".format(volume_id))


if __name__ == '__main__':

    logger = create_logger()

    options = parse_args(sys.argv)

    compose_content = open_compose_file(options['compose_file'])

    volumes = get_volumes(compose_content)

    for vol in volumes:
        backup_volume(volume_id=vol,
                      destination=options['destination'])
    logger.info('Done! Volumes saved: {}'.format(len(volumes)))

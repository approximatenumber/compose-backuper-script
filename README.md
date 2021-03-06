# compose-backuper-script

Script to backup named volumes of your services from docker-compose.yml

It parses `docker-compose.yml`, finds named volume, runs a little container with these volumes mounted inside (`ro`) and saves it to backup file.

Little container is [approximatenumber/compose-backuper](https://hub.docker.com/r/approximatenumber/compose-backuper/).

### Prepare

1. Install needed python modules with `virtualenv`:


```bash
virtualenv compose-backuper
source compose-backuper/bin/activate
pip install -r requirements.txt
```

(When you finish the backup, run `deactivate` to deactivate virtual environment)

2. Pull the image for backup

`docker pull approximatenumber/compose-backuper`

### Usage

Needed arguments:

- `docker-compose.yml` (by default, script searches it in the current directory)
- project name (by default, script takes current directory name)
- destination directory to store backups.

```
usage: compose-backup.py [-h] [-f COMPOSE_FILE] [-p PROJECT_NAME]
                         [-d DESTINATION]

optional arguments:
  -h, --help            show this help message and exit
  -f COMPOSE_FILE, --compose-file COMPOSE_FILE
                        path to docker-compose.yml
  -p PROJECT_NAME, --project-name PROJECT_NAME
                        project name
  -d DESTINATION, --destination DESTINATION
                        destination directory for backups
```

Example:

```bash
python compose-backup.py -f ../opt/app/docker-compose.yml -p myproj -d /opt/backups/

INFO:compose-backup:jenkins-home: saving...
INFO:compose-backup:jenkins-home: saved
INFO:compose-backup:DONE! Volumes saved: 1
```

```bash
ls /opt/backups

myproj_jenkins-home.tar.gz
```

Your contributions are appreciated!

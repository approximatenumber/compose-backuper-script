# compose-backuper-script
Script to backup volumes of your services from docker-compose.yml


### Usage

Just set `docker-compose.yml` (by default, script searches it in current directory) and output directory to store backups.

`python compose-backup.py -f /opt/app/docker-compose.yml -p /mnt/disk/backups`

Then it will automatically find your named volumes and save it.

Example:

```bash
$ python ../compose-backup.py -f ../docker_jenkins/docker-compose.yml -p /opt/backups
INFO:compose-backup:Volume ./jenkins-nginx/conf.d is not a named volume, skipping.
INFO:compose-backup:Volume ./jenkins-nginx/certs is not a named volume, skipping.
INFO:compose-backup:Volume /opt/airt is not a named volume, skipping.
INFO:compose-backup:Volume /var/run/docker.sock is not a named volume, skipping.
INFO:compose-backup:Saving jenkins-master[jenkins-data]...
INFO:compose-backup:Saved jenkins-master[jenkins-data].

$ ls /opt/backups
jenkins-master_jenkins-data.tar.gz
```

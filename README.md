# compose-backuper-script
Script to backup named volumes of your services from docker-compose.yml

### Prepare

Install needed python modules:

`pip3 install -r requirements.txt`

Pull the image for backup

`docker pull approximatenumber/compose-backuper`

### Usage

You need to give it:

- `docker-compose.yml` (by default, script searches it in the current directory)
- project name (by default, script takes current directory name)
- destination directory to store backups.

`python compose-backup.py -f /opt/app/docker-compose.yml -p myproj /mnt/disk/backups`

Then it will automatically find your named volumes and save it.

Example:

```bash
$ python3 compose-backup.py -f ../opt/app/docker-compose.yml -p myproj -d /opt/backups/

INFO:compose-backup:jenkins-home: saving...
INFO:compose-backup:jenkins-home: saved
INFO:compose-backup:DONE! Volumes saved: 1

$ ls /opt/backups

myproj_jenkins-data.tar.gz
```

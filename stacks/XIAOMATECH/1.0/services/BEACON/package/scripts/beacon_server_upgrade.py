import os
import tempfile

from resource_management.core.logger import Logger
from resource_management.core.exceptions import Fail
from resource_management.libraries.functions import tar_archive
from resource_management.core.resources.system import Execute
from resource_management.core.resources.system import Directory

BACKUP_TEMP_DIR = "beacon-upgrade-backup"
BACKUP_DATA_ARCHIVE = "beacon-local-backup.tar"
BACKUP_CONF_ARCHIVE = "beacon-conf-backup.tar"


def post_stop_backup():
    """
    Backs up beacon directories as part of the upgrade process.
    :return:
    """
    Logger.info('Backing up Beacon directories before upgrade...')
    directoryMappings = _get_directory_mappings()

    absolute_backup_dir = os.path.join(tempfile.gettempdir(), BACKUP_TEMP_DIR)
    if not os.path.isdir(absolute_backup_dir):
        os.makedirs(absolute_backup_dir)

    for directory in directoryMappings:
        if not os.path.isdir(directory):
            raise Fail("Unable to backup missing directory {0}".format(directory))

        archive = os.path.join(absolute_backup_dir, directoryMappings[directory])
        Logger.info('Compressing {0} to {1}'.format(directory, archive))

        if os.path.exists(archive):
            os.remove(archive)

        tar_archive.archive_directory_dereference(archive, directory)


def pre_start_restore():
    """
    Restores the directory backups to their proper locations
    after an upgrade has completed.
    :return:
    """
    Logger.info('Restoring Beacon backed up directories after upgrade...')
    directoryMappings = _get_directory_mappings()

    for directory in directoryMappings:
        archive = os.path.join(tempfile.gettempdir(), BACKUP_TEMP_DIR,
                               directoryMappings[directory])

        if not os.path.isfile(archive):
            raise Fail("Unable to restore missing backup archive {0}".format(archive))

        tar_archive.untar_archive(archive, directory)

    # cleanup
    Directory(os.path.join(tempfile.gettempdir(), BACKUP_TEMP_DIR), action="delete")


def _get_directory_mappings():
    """
    Gets a dictionary of directory to archive name that represents the
    directories that need to be backed up and their output tarball archive targets
    :return:  the dictionary of directory to tarball mappings
    """
    import params

    return {params.beacon_local_dir: BACKUP_DATA_ARCHIVE}

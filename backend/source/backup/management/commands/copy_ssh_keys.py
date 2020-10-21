from backup.models import BackupSource
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import logging
import os
import subprocess


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Copies SSH keys to a remote host without any user input'

    def get_ssh_key_path(self):
        return os.path.join(settings.SSH_DIR, 'id_rsa')

    def generate_ssh_keys(self):
        ssh_key_path = self.get_ssh_key_path()
        if os.path.exists(ssh_key_path):
            return

        command = [
            'ssh-keygen', '-b', '2048', '-t', 'rsa', '-f', ssh_key_path, '-q', '-N', '',
        ]
        subprocess.run(command, check=True)

    def copy_ssh_keys(self, user, host, port, password):
        command = [
            'sshpass',
            '-p', password,
            'ssh-copy-id',
            '-o', 'StrictHostKeyChecking=no',
            '-p', str(port),
            '-i', self.get_ssh_key_path(),
            f'{user}@{host}',
        ]
        subprocess.run(command, check=True)

    def add_arguments(self, parser):
        parser.add_argument(
            '-u', '--user',
            help='SSH user on remote host',
            required=True,
            type=str,
        )
        parser.add_argument(
            '-H', '--host',
            help='Remote hostname',
            required=True,
            type=str,
        )
        parser.add_argument(
            '-p', '--port',
            default=22,
            help='SSH port on remote host',
            type=int,
        )
        parser.add_argument(
            '-P', '--password',
            help='SSH password on remote host',
            required=True,
            type=str,
        )

    def handle(self, *args, **options):
        self.generate_ssh_keys()
        try:
            self.copy_ssh_keys(options['user'], options['host'], options['port'], options['password'])
            logger.info(f"SSH keys copied to {options['host']}")
        except:
            logger.exception(f"Failed to copy keys to {options['host']}")
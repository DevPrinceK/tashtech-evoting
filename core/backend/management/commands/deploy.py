import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Automate deployment process'

    def handle(self, *args, **kwargs):
        commands = [
            "source venv/bin/activate",
            "git pull origin main", 
            "python manage.py makemigrations",
            "python manage.py migrate",
            "python manage.py collectstatic --noinput",
            "sudo systemctl restart nginx",
            "sudo service gunicorn restart",
            "sudo service nginx restart"
        ]

        for command in commands:
            self.stdout.write(self.style.SUCCESS(f"Running: {command}"))
            process = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if process.returncode == 0:
                self.stdout.write(self.style.SUCCESS(f"Success: {command}"))
                if command == "sudo service nginx restart":
                    self.stdout.write(self.style.SUCCESS("====================="))
                    self.stdout.write(self.style.SUCCESS("Deployment Successful"))
                    self.stdout.write(self.style.SUCCESS("====================="))
            else:
                self.stderr.write(self.style.ERROR(f"Error running {command}: {process.stderr}"))


# Electronic-Voting Software
E-Voting System for Schools and any democratic organizations

## Getting source code
First clone the project from github or acquire the source code from me via email. <br>
gitub link: git clone https://github.com/DevPrinceK/tashtech-evoting.git

## Installation
Navigate to the tashtech-evoting/core <br>
Command: cd tashtech-evoting/core <br>
<br>
Install dependencies. You may want to create a virtual environment. <br>
Command: pip install -r requirements.txt

## Make Migrations and create superuser
Now make migrations and create a superuser account. <br>
Command 1: python manage.py makemigrations <br>
Command 2: python manage.py migrate <br>
Command 3: python manage.py createsuperuser <br>

After the last command, you will be asked to enter some details to create the superuser account <br>

# Run Server
Now run the server <br>
Command: python manage.py runserver <br>

# Open Software
Now you can access the software locally on your pc via the django local host url <br>
URL: http://127.0.0.1:8000/

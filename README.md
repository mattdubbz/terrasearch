# terrasearch

Real Estate Search

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Install and run the project

- To install and run the project, download directly from the github repo <https://github.com/mattdubbz/terrasearch>

- or clone the repo:

```bash
git clone https://github.com/mattdubbz/terrasearch.git
```

- in the project directory, you should see the two directories terrasearch and env
- activate the virtal enviroment:

```bash
source env/bin/activate
```

- then move into the project root directory:

```bash
ls terrasearch
```

- `ls` in this directory to make sure you see all of the project files.  You should see the manage.py file
- install the local requirements file:

```bash
pip install -r requirements/local.txt
```

- create your PostgreSQL database:

```bash
createdb --username=terraadmin terrasearch
```

- Open a terminal in the projet root directory and run this to read the enviroment variables from the .env file:

```bash
DJANGO_READ_DOT_ENV_FILE=True
```

- make migrations and apply them:

```bash
python manage.py makemigrations
python manage.py migrate
```

- now set up your superuser:

```bash
python manage.py createsuperuser
```

- start the Celery server in a separate terminal:

```bash
celery -A config.celery_app worker -l info
```

- start the Redis server in a separate terminal window:

```bash
redis-server
```

- Run the django server to launch the site and click on the link in the terminal window to open it in the browser:

```bash
python manage.py runserver
```

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

        python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

``` bash
cd terrasearch
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.  This is the projects root directory.

### If there is an error with the database

- If there is an error, run the django_db_reset.sh script:

```bash
sh django_db_reset.sh
```

### Additional commands for working with postgres at the command line

```bash
createdb terrasearch
dropdb -f terrasearch
createuser terraadmin
psql terrasearch
CREATE USER terraAdmin WITH LOGIN PASSWORD 'terrapass';
ALTER ROLE terraadmin WITH SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE terrasearch TO terraAdmin;
# CREATE USER is alias for CREATE ROLE


psql --version
brew services start postgresql      #to start
brew services stop postgresql       #to stop
brew services restart postgresql    #to restart
psql postgres                       #log into postresql service

\du    #list all users
\l    #list all databases
\c [dbname] #connect a database
\q    #quit
\dt   #list all tables in datapase

# to add a role
CREATE ROLE terraAdmin WITH LOGIN PASSWORD 'password';
ALTER ROLE terraAdmin CREATEDB;
```

### Additional Redis commands

```bash
redis-server    #start the redis server
redis-server start
redis-server stop
redis-server restart

#open new terminal for redis cli
redis-cli       #take note of the ip 127.0.0.1:6379

#check to see ifd redis server is running
redis-cli ping  #should return PONG
```

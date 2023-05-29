# Alembic

alembic init <name> -> initialized the alembic version control like git init <name>

alembic revision -m "<message>" -> creates a new revision like git commit -m "<message>"
alembic revision --autogenerate -m "autogenerate votes table" -> use the "--autogenerate" parameter to auto generate all of your reference model from the target_metadata variable in the env.py file ... we can add changes to the models.py file and run this command to upgrade the database

alembic current -> gets the current active revision version git rev-parse origin/master

alembic heads -> gets the newest revisionn version like git rev-parse HEAD

alembic upgrade/downgrade <revision-number from versions folder> -> add new changes to the database like git push

alembic downgrade <down_revision-number from versions folder> -> go to specific revision version like git checkout <commit-hash>

alembic history -> list up all actions like git log



# Deployment Ubuntu

## default installation

sudo apt update && sudo apt upgrade -y -> updates everything, -y is for accepting everything due to the installation process

### second user installation if you just have the root user

adduser <username>

set the password -> skip the FullName, RoomNumber, etc. questions by pressing enter

login with su - <username> -> test to clarify that everything works fine

if everything works login back with root user

usermod -aG sudo <username> -> adding root privileges to the new user

## python and pip installation

sudo apt install python3

sudo apt install python3-pip

check your python version with python3 --version

### if the version is not >= 3.8 then follow these steps:

#### Install Python on Raspberry Pi

wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz -> get python from their website

#### Extract File Contents

tar -zxvf Python-3.8.10.tgz -> extract the contents of the Python-3.8.10.tgz

#### Configure Python Latest Version on Raspberry Pi

cd Python-3.8.10

./configure --enable-optimizations -> configure Python on Raspberry Pi

sudo make altinstall -> build the installation packages for Python on Raspberry Pi

#### Update the Python Version on Raspberry Pi

cd /usr/bin

sudo rm python3

sudo ln -s /usr/local/bin/python3.8 python3 -> link Python placed inside the directory “usr/local/bin”

python3 --version -> check if everything works fine

## python virtualenv package installation

sudo pip3 install virtualenv

## postgresql installation and configuration

sudo apt install postgresql postgresql-contrib -y

sudo su - postgres

psql -U postgres -> adding new user to postgres

\password postgres -> set password

\q -> exit out of the postgres console

exit -> log out the postgres user

cd /etc/postgresql/<version-number>/main -> postgres directory, get version number with cd /etc/postgresql and then type ls

sudo nano postgresql.conf -> under "CONNECTIONS AND AUTHENTICATION" above "#listen_addresses = 'localhost' add listen_addresses = '*' so you can access it from every host

sudo nano pg_hba.conf -> scroll to the bottom and change the 'peer' to 'md5' in the first white line "local   all    postgres   peer" and do the same for the next line "local   all   all   peer". Then change the localhost ip address in the third line from 127.0.0.1/32 to 0.0.0.0/0 and do the same thing for the ipv6 connections from ::1/128 to ::/0

sudo systemctl restart postgresql

test if the changes where saved and login to postgres with psql -U postgres and if you will be ask for a password everything is good to go

## create virtual environment

cd ~ -> go to home directory of your user

mkdir app -> creates our working directory 

cd app -> navigate to the working directory

virtualenv venv -> creates a new virtual environment with the name "venv"

source venv/bin/acitvate -> load the virtual environment and activates it (you can leave it with 'deactivate')

## adding the code to the directory

mkdir src -> creates a src directory in the app directory to store our code

cd src

git clone <github repo link> .

## installing all requirements

start the virtual environment in the app directory before installing the packages

pip3 install -r requirements.txt

sudo apt install libpq-dev

uvicorn app.main:app -> start the app to check if everything installes correct

## adding environment variables

export <env-var-name in capital letters> -> set a new env-variable

printenv -> get all env-variables

unset <env-var-name> -> removes the env-variable

cd ~

touch .env -> creates .env file

ls -la -> check if file is created

sudo nano .env

paste the content from the .env of the github file

set -o allexport; source /home/pi/.env; set +o allexport -> set all environment variables of the .env file. But if you reboot the system all of the environment variables are gone

to avoid this open the .profile file in the home directory and append the command above at the bottom of the file and save it. This will cause the system to set the variables after a reboot

check this by typing exit to the console and reconnect and do printenv

## setup the tables with alembic

alembic upgrade head

## start the app 

uvicorn --host 0.0.0.0 app.main:app -> 0.0.0.0 to make it available to other devices on the same network

if you reboot or the application crashes it wont automatically restart

## install gunicorn

pip3 install gunicorn -> it provides worker which maximize the overall performance and it supports various load balancing techniques

pip install httptools -> helper libary for gunicorn

pip install uvloop -> helper libary for gunicorn

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 -> start gunicorn but note that you have to be in your virtual environment

## create a service for gunicorn

cd /etc/systemd/system

sudo nano <service-name>.service -> file with the gunicorn.service file content

systemctl start <service-name>

systemctl status <service-name> -> check if everything is correct

## set the service to start right after booting

sudo systemctl enable <service-name> -> active the start after boot function

# setup the nginx server

sudo apt install nginx

systemctl start nginx

default configuration in /etc/nginx/sites-available/
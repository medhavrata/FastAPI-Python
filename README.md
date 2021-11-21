# FastAPI-Python

This repo is to build FastAPI(Python Framework)

---

Create and activiate the virtual environment for python:

python3 -m venv venv
source venv/bin/activate

---

## How to build the RestAPI using FastAPI:

- FastAPI is a Python framework to build the RestAPI
- It will run the application as an API endpoint and will access the online requests from frontend
- Frontend can do the CRUD operations via GET/POST/PUT/DELETE
- Need to ensure that the schema is being defined for frontend to send the data
- Need to ensure that the correct HTTP response code is being sent back to frontend
- Define the Environmental Variables
- Can use "alembic" to create the Postgres tables

### Once the Application is ready:

- Push the changes to GitHub, remember to create the .gitignore file so that don't push the confidential data to GitHub
- App can be hosted on Heroku(PAAS):

  - Install Heroku
  - Push the changes to Heroku using the same Git Commands
  - Create the "Procfile", which will contain the command to start the App
  - Run alembic command to create the tables
  - Define the Environmental Variables in Heroku
  - App will be started by Heroku, once the changes will be pushed

- App can be installed on VM (IAAS)

  - Create an Ubuntu VM
  - Update the VM(sudo apt update && sudo apt upgrade) and install python3/pip3/virtualenv
  - Install postgresqul (sudo apt install postgresql postgresql-contrib)
    - Above installation will install the CLI for postgresql as well to interact with DB - psql
    - It will create a postgres DB user named 'postgres' and a group named 'postgres'
    - Try to connect with postgres db using: $ psql -U postgres
      - An error will come: psql: error: FATAL: Peer authentication failed for user "postgres"
      - Above error is coming becuase by default on Ubuntu, while connecting to postgres db, it will check that the user logged in
        must be the same as being passed in the -U flag.
      - In the above command, logged in user is 'root' and trying to connect with db as user 'postgres', and that's why this error
    - Change the user to postgres user: $ su - postgres
    - Connect with the postgres db now: $ psql -U postgres
    - Once connected, set a password for postgres user:
      - command is: $ \password postgres
    - now can exit from postgres db cli: \q
  - To change the configuration settings for postgresql, go to directory: $ /etc/postgresql/12/main
  - Two main files to update the configuration are: postgresql.conf, pg_hba.conf
  - To update the connection settings, open postgresql.conf and in 'CONNECTIONS AND AUTHENTICATION' update listen_addresses = '\*'
  - To update the autentication settings and network settings, open pg_hba.conf and update the autentication method from peer to md5 and update the IP addresses
  - Restart the db so that changes will be in effect: $ systemctl restart postgresql
  - As a best practice, add a user to run the application rather than running the App with root user
  - This new user by default will not have the sudo access, so provide the sudo access
  - $ usermod -aG sudo username
  - Create a directory in home directory (can be created anywhere) to clone the code from GitHub
  - Install the required packages from requirements.txt file
  - Now set the environment variables:
    - Go to home directory and create .env (don't create the environment file in the same directory in which app files, might be checked in to Git)
    - Just provide the environment variables without EXPORT keyword
    - As the EXPORT keyword is not mentioned in front of environment variables, so need to run the below command:
    - $ set -o allexport; source /home/testpostgres/.env; set +o allexport
    - Need to put this command in ~/.profile , so that the environment variables can be set whenever machine reboots
  - Create a database using pgAdmin
  - Run the alembic upgrade head -> It will create the tables
  - Start the Application using: uvicorn --host 0.0.0.0 app.main:app
  - If we don't use --host 0.0.0.0, the app will listen only on localhost
  - Currently the application will not restart, so install 'pip install gunicorn', it will restart the application
  - If gets any issue while installing gunicorn, install httptools and uvloop
  - Start the Application via gunicorn -> $ gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
  - It will start the application with 4 Worker Nodes and will listen on any IP
  - Currently the App has been started manually, but it should be started automatically as the machine starts
    - We need to create a Service to do this
    - We can see all the services at /etc/systemd/system/
    - Create a new service for the application: $ sudo vi fastapi.service
    - Start the applicatation: $ systemctl start fastapi
    - It will fail as this will not be able to access the enviornment variables
    - Need to amend the service file to mention (EnvironmentFile) from where the environment variables to pick
    - Run: $ systemctl restart fastapi
    - To enable the restart of application: $ sudo systemctl enable fastapi

- Application is being deployed on the VM and the user interacting with the App directly, but it is not optimized solution.
- We can use nginx web server to act as a proxy for our application
- Install nginx on the server and nginx will recieve all the requests (http/s) and will do SSL termination as well and send http request to application
- By doing so, we don't need to put all this logic in our Application
- $ sudo apt install nginx
- After installing, go to server ip address and it will load the nginx default page
- To change the default page settings, go to: $ cd /etc/nginx/sites-available/
- Check the settings in default config file
- We can update the location in default config file to act as a proxy
-         location / {
                proxy_pass http://localhost:8000;
- This change is: whatever comes to root path and beyond to nginx, pass that traffic to localhost:8000, where our app is running
- Optionally, we can setup a domain name which will point to the server and can setup the SSL for the domain name
- Next, we need to setup the firewall rules on the server, using ufw (Uncomplicated FireWall)
- run $ sudo ufw status , it will show the currently applied firewall rules
- to set the rules run, $ sudo ufw allow http / sudo ufw allow https / sudo ufw allow ssh
- to delete a run, in case, sudo ufw delete allow http

## Done Some changes locally

- Push the changes to GitHub
- Pull the changes at Server
- Restart the service (systemctl restart fastapi)

## We can containerized the App

- Build a Docker Image of App using Python as Base Image
- Create a docker-compose file to run the container and pass the environment variables
- Use the Postgres image in the docker-compose file, so that both application and database will run in container

## Local changes will not be pushed to application running in Container

- If we make any local changes, those will not be reflected in the container
- To sync this, we can use the bind volumne and bind the local directory to container directory
- This will sync any local changes in the container as well
- Use: volumes: - ./:/usr/src/app:ro
- The last option is ro(read only), so container can't change anything in this directory
- Give the command option in docker-compoase as well to reload the application
- Now we can push the application image to Docker Hub, from where it can be pulled by production server
- But we need to create two separate docker-compose file, one for dev and one for prod
- In the dev docker-compose file, we are building an image and in prod we are pulling an image

## Building the Testing for our Application using PYTEST

- Use the PYTEST/testclient library to do the testing
- Create the file to include the test functions with name test-\*.py
- Testclient works similar to 'requests' libaray where we can make the calls to a specific route
- But we need to make a separate testing database rathar than messing up with the development database
- To do this, we can create a test database instance in the testing file and use the instnace
- Provide the database details in the testing file, it can be local testing database, might be running in container or on the cloud
- While testing using pytest:
  - We can create the fixtures, it is a function which other functions can inherit
  - We can also parameterize the tests

### Build a CI/CD pipeline using Github Actions

- Setup a Github Actions workflow job
- Need to setup the environment variables so that tests can run, there are three ways:
  - Set the environment variables in the workflow using hardcoded values
  - Set in Github, Settings -> Secrets, but this will set it globally
  - Set in Github, Settings -> Environments, this is a better way which will set as per the environment
- Need to setup the postgres database for testing to complete
  - Need to mention the step in workflow file to run the postgres container first and then the tests
- Next, create a docker image from GitHub and push to Docker Hub from where the production server can pull the Image
- For creating a docker image via github actions, you need docker hub access token, which is not available on free account
- Setup a separate job for CD in the github workflow files
- Look for some actions from GitHub Marketplace to use to deploy the changes to Heroku

#### Some Issues to tackle :

- sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) SCRAM authentication requires libpq version 10 or above(while running postgresql
  from container)
- Created one additional alembic version, need to figure out how to delete that one (b25644a3ef6c)

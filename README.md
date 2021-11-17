# FastAPI-Python

This repo is to build FastAPI(Python Framework)

---

Create and activiate the virtual environment for python:

python3 -m venv venv
source venv/bin/activate

---

How to build the RestAPI using FastAPI:

- FastAPI is a Python framework to build the RestAPI
- It will run the application as an API endpoint and will access the online requests from frontend
- Frontend can do the CRUD operations via GET/POST/PUT/DELETE
- Need to ensure that the schema is being defined for frontend to send the data
- Need to ensure that the correct HTTP response code is being sent back to frontend
- Define the Environmental Variables 
- Can use "alembic" to create the Postgres tables

Once the Application is ready:

- Push the changes to GitHub, remember to create the .gitignore file so that don't push the confidential data to GitHub
- App can be hosted on Heroku:
  - Install Heroku 
  - Push the changes to Heroku using the same Git Commands
  - Create the "Procfile", which will contain the command to start the App
  - Run alembic command to create the tables
  - Define the Environmental Variables in Heroku
  - App will be started by Heroku, once the changes will be pushed

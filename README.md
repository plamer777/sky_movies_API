# The Sky Movies API
This application is an API for kind of kinozal services.

The app provides functionality as follows:
 - Register and login a user
 - Update user data 
 - Retrieve directors, movies and genres 
 
---

**Technologies used in the project:**
 
 - Flask 2.2.2
 - Flask-RESTX 1.0.5
 - SQLAlchemy 1.4.46
 - PyJWT 2.4.0
 - pytest 7.2.1
 - Gunicorn 20.1.0
 - Flask-Cors 3.0.10
 - Flake8 6.0.0 
 - Docker
 - Docker-compose

---

**Project's structure:**
 
 - .github - CI/CD yaml file to deploy the app
 - project/dao - data access objects to work with database
 - project/services - service objects with business logic
 - project/setup - db initialization, db base model, flask-restx parsers and schemas
 - project/static - static files
 - project/templates - project html templates and images
 - project/views - CBVs for all necessary routes
 - project/constants.py - constants to configure the application
 - project/models.py - db models
 - project/server.py - functions to initialize the Flask app - 
 - tests - project tests
 - project/container.py - DAO and Service instances
 - Docker-compose-ci.yaml - docker-compose template file
 - Dockerfile_ci - a template Docker file
 - fixtures.json - data to fill up database
 - create_tables.py and load_fixtures.py - functions to create db tables and fill it up 
 - run.py - a main file to start the app
 - project/utils.py - utility functions
 - requirements.txt - project dependencies
 - requirements.dev.txt - project dependencies for development purposes
 - README.md - this file with project description
---

**How to start the project:**
The app is ready to install out of the box by using GitHub actions. 
To start the app just follow the next steps:
 - Prepare VPS where you are going to deploy the app (I recommend to use Ubuntu. 
You'll need a username and password) 
 - Clone this repository and remove branches-ignore section from app_deploy.yaml file
 - Install docker and docker-compose packages by the command `sudo apt install docker.io docker-compose` 
on your VPS
 - Prepare .env_ci file if you need to change something
 - Push this project to your new repository and wait while deploying will be done
 - After that application is ready to process requests

**Necessary GitHub secrets:**

![img.png](promo/img.png)

The project was created by Alexey Mavrin in 04 December 2022
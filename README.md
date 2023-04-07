# Django BoilerPlate Project

## Table of contents

* [Objective of the project](#objective-of-the-project)
* [Prerequities](#prerequities)
* [Configure the project in local environment](#configure-the-project-in-local-environment)
* [Rename the project](#rename-the-project)
* [Contributing Guidelines](#contributing-guidelines)
* [Command to start the application using docker](#command-to-start-the-application-using-docker)
* [Commands to start the application without docker](#commands-to-start-the-application-without-docker)
* [Sentry Integration with the application](#sentry-integration-with-the-application)


## Objective of the project
Django Boilerplate project which might help developer to start a new Django project by reusing some valuable work provided by open-source enthusiasts very quickly.


## Prerequities
* Python > 3.8.*
* postgresql

## Configure the project in local environment
* Clone the project from the reposetory [https://bitbucket.org/simformteam/python-internal-projects-django-boilerplate/src/master/](https://bitbucket.org/simformteam/python-internal-projects-django-boilerplate/src/master/)
* Create virtual environment
* Get pull in your local branch from the `dev` branch for the latest code base.
* Checkout to the `dev` branch for the latest code base
* Install requirements from `requirements.txt` file.
* Update the `.env` file with required local credentials details, one can take reference from the `.env.example` file.

## Rename the project
* By default the boilerplate project have name set as `config`, if developer wants to change it with any other specific name then one can use management command for the same.
```
python manage.py rename_project <<config(current project name)>> <<new project name>>
```

## Contributing Guidelines
* Run command `pre-commit install`. Run this command from your git init root.
* Run command `pre-commit run -a`. This command will check python files and give result regarding formatting.
* After installing pre-commit hook, on each commit it will verify code standard formatting and will allow you to commit if all checks are passed.
* If you added these configs to an existing project, you may want to format whole code from the start. So for that, you just need to run command `pre-commit run --all-files`.

## Command to start the application using docker
```
 docker-compose up --build
````

## Commands to start the application without docker
```
python manage.py runserver
```
## Sentry Integration with the application
Sentry Django integration enables automatic reporting of errors and exceptions for the application.
- SignUp or SignIn from given URL:
    [https://sentry.io/welcome/](https://sentry.io/welcome/?utm_source=google&utm_medium=cpc&utm_campaign=9657410528&utm_content=g&utm_term=sentry&device=c)
- Click on **Create Project** button.
- Choose your platform i.e. **DJANGO** for this application.
- Add project name and click on **Create Project** button.
- Get **dsn** url of your project and set it for environment value of **SENTRY_DSN**.
    - Note: One can also find this **dsn** value from,
    Settings > Projects > (select your project) > SDK SETUP > Client Keys (DSN)
- Set the name of environment for **SENTRY_ENV** environment variable e.g. **development, Staging, production** etc. This helps a user to filter issues, releases, and user feedback.

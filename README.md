# Turing Back End Challenge
To complete this challenge, you need to ensure all route returns a similar response object as described in our API guide. To achieve this goal, you will have to fix the existing bugs, implement the incomplete functions, and add test cases for the main functions of the system.

## Getting started

### Prerequisites

In order to install and run this project locally, you would need to have the following installed on you local machine.

* [**Python 3+**](https://www.python.org/downloads/release/python-368/)
* [**Django 2+**](https://www.djangoproject.com/download/) 
* [**MySQL**](https://www.mysql.com/downloads/)


### Installation

* Clone this repository
* Navigate to the project directory `cd src/`
* Create a virtual environment
* Install dependencies `pip3 install -r requirements.txt`

* Edit `src/turing_backend/settings.py` database credentials to your database instance

* Create a MySQL database and run the sql file in the database directory to migrate the database
`mysql -u <dbuser> -D <databasename> -p < ./sql/database.sql`

* Run the command `python manage.py makemigrations` 

* Run the command `python manage.py migrate` to create and sync the mysql database (you must have the database previously created with name 'turing_db').

* It's needed that you have your own super user to admin the application, so run the command `python manage.py createsuperuser` and follow the instructions.

* Run the command `python manage.py runserver`

* Run development server

`python manage.py runserver`		

## Request and Response Object API guide for all Endpoints

* Check [here](https://docs.google.com/document/d/1J12z1vPo8S5VEmcHGNejjJBOcqmPrr6RSQNdL58qJyE/edit?usp=sharing)
* Visit `http://127.0.0.1:80/docs/

## Using Docker 
Build image

`docker build -t turing_app .` 



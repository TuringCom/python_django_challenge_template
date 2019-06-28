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

* Navigate to the project directory ```cd src/```

* Install dependencies

			```pip install -r requirements.txt```

* Edit `src/backend/settings.py` database credentials to your database instance

* Create a MySQL database and run the sql file in the database directory to migrate the database
			```mysql -u <dbuser> -D <databasename> -p < ./sql/database.sql```

* Run development server

			```python manage.py runserver```

## Request and Response Object API guide for all Endpoints

* Check [here](https://docs.google.com/document/d/1J12z1vPo8S5VEmcHGNejjJBOcqmPrr6RSQNdL58qJyE/edit?usp=sharing)


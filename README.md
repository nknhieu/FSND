## Full Stack Web Developer Nanodegree (nd0044 v2)
This is the public repository for Udacity's Full-Stack Nanodegree program. Here, you can find starter-code the following projects:

* *01_fyyur/starter_code* - This is the project from C1. SQL and Data Modeling for the Web
* *02_trivia_api/starter* - This is the project from C2. API Development and Documentation
* *03_coffee_shop_full_stack/starter_code* - This is the project from C3. Identity and Access Management
* *capstone* - This is the final project of this Nanodegree.

Feel free to suggest edits in the current repo by raising a PR.

# Casting Agency Project
Udacity Full-Stack Web Developer Nanodegree Program Capstone Project

## Project Motivation
Our Car Rental app offers a seamless and convenient way to rent vehicles for various needs. Whether you're planning a road trip, a business visit, or simply need a temporary vehicle, our app has got you covered. With a user-friendly interface and a wide range of vehicles to choose from, you can easily find and book the perfect car for your journey.


This project is simply a workspace for practicing and showcasing different set of skills related with web development. These include data modelling, API design, authentication and authorization and cloud deployment.

## Getting Started

The project adheres to the PEP 8 style guide and follows common best practices, including:

* Variable and function names are clear.
* Endpoints are logically named.
* Code is commented appropriately.
* Secrets are stored as environment variables.


### Key Dependencies & Platforms

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Auth0](https://auth0.com/docs/) is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways

- [PostgreSQL](https://www.postgresql.org/) this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.

- [Heroku](https://www.heroku.com/what) is the cloud platform used for deployment


### Running Locally

#### Installing Dependencies

##### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Database Setup
With Postgres running, restore a database using the `capstone.psql` file provided. In terminal run:

```bash
createdb capstone
psql capstone < capstone.psql
```

#### Running Tests
To run the tests, run
```bash
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python test_app.py
```

Optionally, you can use `run_test.sh` script.

#### Auth0 Setup

You need to setup an Auth0 account.

Environment variables needed: (setup.sh)

```bash
export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com" # Choose your tenant domain
export ALGORITHMS="RS256"
export API_AUDIENCE="capstone" # Create an API in Auth0
```

##### Roles

Create three roles for users under `Users & Roles` section in Auth0

* User Role:
	* Permissions: Can view information about vehicles, customers, and rentals.
* Admin Role:
  * Permissions (User Role permissions included):
  * Add new vehicles to the database.
  * Delete vehicles from the database.
  * Edit information about vehicles.
  * Add new customers to the database.
  * Delete customers from the database.
  * Edit information about customers.
  * Create new rental records.
  * Edit existing rental records.
  * Delete rental records.

##### Permissions

Following permissions should be created under created API settings.

* `view:vehicle`
* `view:customers`
* `view:rental`
* `delete:vehicle`
* `delete:customers`
* `post:vehicle`
* `post:customers`
* `post:rental`
* `update:vehicle`
* `update:customers`
* `get:vehicle`
* `get:customers`
* `get:rental`

##### Set JWT Tokens in `auth_config.json`

Use the following link to create users and sign them in. This way, you can generate 

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

#### Launching The App

1. Initialize and activate a virtualenv:

   ```bash
   virtualenv --no-site-packages env_capstone
   source env_capstone/bin/activate
   ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Configure database path to connect local postgres database in `models.py`

    ```python
    database_path = "postgres://{}/{}".format('localhost:5432', 'myFSND')
    ```
**Note:** For default postgres installation, default user name is `postgres` with no password. Thus, no need to speficify them in database path. You can also omit host and post (localhost:5432). But if you need, you can use this template:

```
postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
```
For more details [look at the documentation (31.1.1.2. Connection URIs)](https://www.postgresql.org/docs/9.3/libpq-connect.html)

4. Setup the environment variables for Auth0 under `setup.sh` running:
	```bash
	source ./setup.sh 
	```
5.  To run the server locally, execute:

    ```bash
    export FLASK_APP=flaskr
    export FLASK_DEBUG=True
    export FLASK_ENVIRONMENT=debug
    flask run --reload
    ```

    Optionally, you can use `run.sh` script.

## API Documentation

### Models
There are two models:
Vehicle:
    brand
    model
    year
    color
    phone
    rentalprice

Customer:
    firstname
    lastname
    email
    phone
    address

Rental:
    vehicle_id
    customer_id
    rentaldate
    returndate
    totalcost

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error

### Endpoints


#### GET /vehicles 
* Get all vehicle

* Require `view:vehicle` permission

* **Example Request:** `curl 'http://http://127.0.0.1:5000/vehicle'`


	
#### GET /customers 
* Get all customers

* Requires `view:customers` permission

* **Example Request:** `curl 'http://http://127.0.0.1:5000/customers'`

deployment_webservice

render_URI = `https://render-deployment-projectfsnd.onrender.com``

# storm-benefits-internship-api-technical-exam

A simple API implemented in Python with basic CRUD functionalities and wildcard search functions.

## Dependencies

1. Flask (Framework used)
2. flask_sqlalchemy (ORM for the database)
3. flask_marshmallow (Library for serialization/deserialization; used in this project to render json responses)
4. marshmallow_sqlalchemy
5. pymysql

## Install

Run the following on the command line to install the dependencies of the project:
```bash
pip install -r requirements.txt
```

Create a MySQL database with the name 'companies' and export 'company.sql'

## Run

Run the program by typing the following into the command prompt:
```bash
python companyCRUD.py
```

### Built with
1. Flask
2. XAMPP (web server and MySQL server used)
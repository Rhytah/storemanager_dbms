# storemanager_dbms

[![Build Status](https://travis-ci.com/Rhytah/storemanager_dbms.svg?branch=develop)](https://travis-ci.com/Rhytah/storemanager_dbms)

[![Coverage Status](https://coveralls.io/repos/github/Rhytah/storemanager_dbms/badge.svg?branch=develop)](https://coveralls.io/github/Rhytah/storemanager_dbms?branch=app-tests)

[![Maintainability](https://api.codeclimate.com/v1/badges/32ed8c7262442003a252/maintainability)](https://codeclimate.com/github/Rhytah/storemanager_dbms/maintainability)

### Tools

* Text editor where we write our project files. (VScode)
* Flask Python Framework -Server-side framework
* Pytest       - a Python Testing Framework
* Pylint       - a Python linting library 
* Postgresql   - Database to store data
* Postman      - Application to test and consume endpoints
* PEP8         - Style guide
* PgAdmin      - Graphical User interface. Management tool for postgresql database

**Getting Started**
clone the github repo to your computer:
* $git clone https://github.com/Rhytah/storemanager_dbms.git

* Extract the zip file to another file

**Create virtual environment and activate it**
```
$pip install virtualenv
$ virtualenv venv
$ venv\Scripts\activate
``` 
 **Install all the necessary tools by**
 ```
 $pip insatll -r requirements.txt
 ```
**Start app server in console/terminal/commandprompt**
```
$python app.py
```
**Test app in terminal**
```
$pytest             -run python tests
$pytest --cov       -check test coverage for pytests
```
## Versioning
```
This is version two "v2" of the API
```
## End Points(Required Features)
|           End Point                                 |            Functionality                   |
|   -----------------------------------------------   | -----------------------------------------  |
|     POST api/v2/auth/login                          |             Login to application           |
|     POST api/v2/auth/signup                         |             Admin add a user account       |
|     POST api/v2/products                            |             Create a product               |
|     GET  api/v2/products                            |             Fetch all products             |
|     GET  api/v2/products/<int:productId>            |             Fetch a product                |
|     POST api/v2/sales                               |             Add a sale order               |
|     GET  api/v2/sales/<int:saleId>                  |             Fetch a specific sale order    |
|     GET  api/v2/sales                               |             Admin fetch all sale orders    |

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/f50315624db4ad24d6f5)

## Hosted app url
- https://storemanager-dbms.herokuapp.com/

## Author
- [Rhytah] https://github.com/Rhytah
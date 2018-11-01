from smapi import app
from flask import Flask
from config import app_configuration
from smapi.models.dbase import Databasehandler
db=Databasehandler()  

if __name__=='__main__':
    app.run(debug=True, port=5000)
    db=Databasehandler()
    #
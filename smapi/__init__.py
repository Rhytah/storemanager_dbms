from flask import Flask


app = Flask(__name__)

from smapi.models.dbase import Databasehandler
from smapi.views import auth_views, product_views,sale_views

if __name__ == '__main__':
    app.run()
    db=Databasehandler()
    db.connect()
    db.create_tables()
    app.config['JWT_SECRET_KEY'] = 'andela13'  
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] =False


@app.route('/')
@app.route('/index')
def index():
    return "StoreManager App. Manage your Products and Sales efficiently using DBMS"
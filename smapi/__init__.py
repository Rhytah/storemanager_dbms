from flask import Flask


app = Flask(__name__)

from smapi.models.dbase import Databasehandler
from smapi.views import auth_views, product_views,sale_views

if __name__ == '__main__':
    app.run()
    db=Databasehandler()
    db.connect()
    db.create_tables()


@app.route('/')
@app.route('/index')
def index():
    return "StoreManager App. Manage your Products and Sales efficiently using DBMS"
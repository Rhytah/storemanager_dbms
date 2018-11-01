from flask import Flask

from config import app_configuration
from flask_jwt_extended import JWTManager
from smapi.models.dbase import Databasehandler 


def create_app(mode):
    app = Flask(__name__)
    # app.config.from_pyfile('config.py')
    app.config.from_object(app_configuration[mode])
    jwt = JWTManager(app)

    from smapi.views.auth_views import auth 
    from smapi.views.sale_views import sale
    from smapi.views.product_views import product

    app.register_blueprint(auth)
    app.register_blueprint(sale)
    app.register_blueprint(product)

    return app

app=create_app(mode='testing')
# db = Databasehandler()

# from .views import auth_views,sale_views,product_views

if __name__ =='__main__':
    app.run()
    
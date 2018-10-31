from flask import Flask

from config import app_configuration


def create_app(mode):
    app = Flask(__name__)
    # app.config.from_pyfile('config.py')
    app.config.from_object(app_configuration[mode])
    
    return app

app=create_app(mode='testing')


from .views import auth_views,sale_views,product_views

if __name__ =='__main__':
    app.run()

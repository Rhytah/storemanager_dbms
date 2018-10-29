from flask import Flask


app = Flask(__name__)


from smapi.views import auth_views, product_views,sale_view

if __name__ == '__main__':
    app.run()
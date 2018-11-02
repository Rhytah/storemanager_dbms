import re

class Validation:

    def user_validate(self, username, password,role):
        if not username:
            return "usename is missing"
        if username == " ":
            return "username is missing"
        if not re.match(r"^([a-zA-Z\d]+[-_])*[a-zA-Z\d*]+$", username):
            return "username must have no white spaces"

        if (role != "true" and role != "false"):
            return "role should either be true for admin-user  or false for attendant-user"    
        if len(username) < 4:
            return "username should be more than 4 characters long"
        if not password:
            return "password is missing"

    def login_credits(self, username, password,role):
        if not username:
            return "username is missing"
        if not password:
            return "password is missing" 
        if not role:
            return "role is missing"
    
    def product_validate(self, product_name, unit_price,category,stock):
        if not product_name:
            return "product name is missing"
        if product_name == " ":
            return "product name is missing"
        if not category:
            return "category is missing"
        if category == " ":
            return "category is missing"
        if not re.match(r"^([a-zA-Z]+[-_\s])*[a-zA-Z]+$", product_name):
            return "product name must have no white spaces"
        if not re.match(r"^([a-zA-Z]+[-_\s])*[a-zA-Z]+$", category):
            return "category must have no white spaces"
        if len(category) < 2:
            return "category should be descriptive, write a meaningful category title"
        if not re.match(r"^[0-9]*$", stock):
            return "stock must be only digits and must have no white spaces"
        if not re.match(r"^[0-9]*$", unit_price):
            return "price must be only digits and must have no white spaces"    
        if len(product_name) < 2:
            return "product name should be more than 4 characters long, write a meaningful name"
        if not stock:
            return "stock is missing"
        if stock == " ":
            return "stock is missing"
        if int(stock) < 1:
            return "stock should be at least 1 item"    
        if not unit_price:
            return "unit_price is missing"
        if int(unit_price) < 1:
            return "unit price should be greater than zero"    
        if unit_price == " ":
            return "unit_price is missing" 

    def sale_validate(self, product_id, entered_by,quantity):
        if not product_id:
            return "product Id field is missing"
        if product_id == " ":
            return "product Id field is missing"
        if not entered_by:
            return "Name of attendant field is missing"
        if entered_by == " ":
            return "Who is making sale, consider input of name"
        if not re.match(r"^([a-zA-Z]+[-_\s])*[a-zA-Z]+$", entered_by):
            return "product name must have no white spaces"
        if not re.match(r"^[0-9]*$", quantity):
            return "quantity must be only digits and must have no white spaces"
        
        if not quantity:
            return "quantity is missing"
        if quantity == " ":
            return "quantity is missing"
        if int(quantity) < 1:
            return "quantity should be at least 1 item"    

    def product_mod(self, product_name, unit_price,stock):
        if not product_name:
            return "product name is missing"
        if product_name == " ":
            return "product name is missing"
        
        if not re.match(r"^([a-zA-Z]+[-_\s])*[a-zA-Z]+$", product_name):
            return "product name must have no white spaces"
        
        if not re.match(r"^[0-9]*$", stock):
            return "stock must be only digits and must have no white spaces"
        if not re.match(r"^[0-9]*$", unit_price):
            return "price must be only digits and must have no white spaces"    
        if len(product_name) < 2:
            return "product name should be more than 4 characters long, write a meaningful name"
        if not stock:
            return "stock is missing"
        if stock == " ":
            return "stock is missing"
        if int(stock) < 1:
            return "stock should be at least 1 item"    
        if not unit_price:
            return "unit_price is missing"
        if int(unit_price) < 1:
            return "unit price should be greater than zero"    
        if unit_price == " ":
            return "unit_price is missing" 
    def category_validate(self, category):
        if category == " ":
            return "category is missing"
        if not re.match(r"^([a-zA-Z]+[-_\s])*[a-zA-Z]+$", category):
            return "category must have no white spaces"
        if len(category) < 2:
            return "category should be descriptive, write a meaningful category title"
        if not category:
            return "category is missing"

            
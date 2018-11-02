import psycopg2
import re
import os
from psycopg2.extras import RealDictCursor
from flask import current_app as app



class Databasehandler:
    
    def __init__(self):
        
        self.conn =psycopg2.connect(dbname="store_db", user="postgres", host="localhost", password="")
        self.cursor=self.conn.cursor(cursor_factory=RealDictCursor)
        self.conn.autocommit = True
    # def startdb(self):
        try:
            
            connection_credentials= """
                    dbname='store_db' user= 'postgres' host='localhost' 
                    """
            
            connection_credentials1="""
                    dbname='test_db' user= 'postgres' host='localhost' 
                    """
                
            if app.config.get('ENV') == 'development':
                print(app.config.get('DATABASE_URI'))
                self.conn = psycopg2.connect(connection_credentials)
                self.conn.autocommit = True
                self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("\n\n Database Connected\n\n")

            if app.config.get('ENV') == 'testing':
                print(app.config.get('DATABASE_URI'))
                self.conn = psycopg2.connect(connection_credentials1)
                self.conn.autocommit = True
                self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
                print("\n\n Database Connected\n\n")
                            
        except Exception as e:
            print(e)
            print("Connection failed")


        usercmd="""CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY,
            username VARCHAR (30),
            password VARCHAR (10),
            role BOOLEAN DEFAULT FALSE NOT NULL)"""
        self.cursor.execute(usercmd)
    
        pdtcmd="""CREATE TABLE IF NOT EXISTS products(
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(20),
            unit_price INT,
            category VARCHAR(15),
            stock INT)"""
        self.cursor.execute(pdtcmd)
        salecmd="""CREATE TABLE IF NOT EXISTS sales(
            sale_id SERIAL PRIMARY KEY ,
            entered_by VARCHAR,
            product_id INT REFERENCES products (product_id),
            cost INT,
            quantity INT,
            total INT)"""
        self.cursor.execute(salecmd)
        adminuser=f"""
                INSERT INTO users(username, password, role)
                VALUES('admin','admin' ,TRUE)
                """
        self.cursor.execute(adminuser)


    def search_user(self,username):
        cmd="SELECT * FROM users WHERE username='{}'".format(username)
        self.cursor.execute(cmd)
        result=self.cursor.fetchone()
        if result:
            return result
        else:
            return {"message":"User doesn't exist"}


    def add_pdt(self,product_name,unit_price,category,stock):
        cmd="INSERT INTO products(product_name,unit_price,category,stock) VALUES ('{}','{}','{}','{}');".format(product_name,unit_price,category,stock)
        self.cursor.execute(cmd)


    def get_pdts(self):
        cmd ="SELECT * FROM products;"
        self.cursor.execute(cmd)
        allproducts = self.cursor.fetchall()
       
        return allproducts

    def get_a_pdt(self,product_id):
        product = None
        cmd="SELECT product_name,unit_price FROM products WHERE product_id = {};".format(product_id) 
        self.cursor.execute(cmd)
        product =self.cursor.fetchone()
        if product is not None:
            return product
        return {"message":"Id non-existent, enter valid product Id"}

    def get_sales(self):
        cmd ="SELECT * FROM sales;"
        self.cursor.execute(cmd)
        sales = self.cursor.fetchall()
        return sales
        
    def get_a_sale(self,sale_id):
        sale= None
        cmd="SELECT * FROM sales WHERE sale_id = {};".format(sale_id) 
        self.cursor.execute(cmd)
        sale =self.cursor.fetchone()

        if sale is not None:
            return sale
        return {"message":"Id non-existent, enter valid sale Id"}

    def delete_product(self,product_id):
        # dpdt=None
        del_cmd="DELETE FROM products WHERE product_id={}".format(product_id)
        dpdt=self.cursor.rowcount
        self.cursor.execute(del_cmd)
    
        if dpdt:
            return dpdt
        else:
            return {"message":"Product doesn't exist"}

    def modify_product(self,unit_price,product_id):
        sql = "UPDATE products SET unit_price = '{}' WHERE product_id = '{}';".format(unit_price,product_id)
        updated_rows = 0    
        self.cursor.execute(sql)
        updated_rows = self.cursor.rowcount
        self.conn.commit()
        return updated_rows

    def add_user(self,username,password):
        cmd="""INSERT INTO users(username,password) 
        VALUES ('{}','{}');""".format(username,password)
        self.cursor.execute(cmd)

    def promote_user(self,user_id,role):
        cmd= "UPDATE users SET role = '{}' WHERE user_id= '{}';".format(role,user_id)
        updated_rows = 0    
        self.cursor.execute(cmd)
        updated_rows = self.cursor.rowcount
        return updated_rows

    def get_users(self):
        usercmd ="SELECT * FROM users;"    
        self.cursor.execute(usercmd)
        users = self.cursor.fetchall()
        return users

    def drop_table(self,table_name):        
        drop_table = "DROP TABLE IF EXISTS {} CASCADE".format(table_name)
        result=self.cursor.execute(drop_table)
        return result

    def create_saleorder(self,product_id,entered_by,cost,quantity,total):
        sql = "INSERT INTO sales(product_id,entered_by,cost,quantity,total) \
            VALUES ('{}','{}','{}','{}',{})".format(product_id,entered_by,cost,quantity,total)
        result= self.cursor.execute(sql)
        if result:
            return result
        return {"Key-Error": "Product you are trying to sell is unavailable. Enter valid Product Id"}

    def add_sale(self,product_id,entered_by,cost,quantity,total):
        product_query = f"""
            SELECT * from products
            WHERE product_id = {product_id} """
        self.cursor.execute(product_query)
        returned_product =self.cursor.fetchone()

        sale_query = f"""
            INSERT INTO sales (product_id,entered_by, cost,quantity, total)
            VALUES (, {product_id}, {entered_by},{quantity}, {total})
        """
        total = (quantity * returned_product['unit_price'])
        new_stock = (returned_product['stock'] - ['quantity'])

        update_stock = f"""
        UPDATE products SET quantity={new_stock}
        WHERE product_id={product_id}
        """        
        self.cursor.execute(update_stock)
        self.cursor.execute(sale_query)

        response = {'message':'Sales record saved successfully'}
        return response
        
        
    def update_product(self, product_id,product_name, unit_price, stock):
        #function to update product
        try:
            query = ("""UPDATE products SET product_name = '{}', unit_price = '{}', stock = '{}'  where product_id = '{}'""" .format(
                product_name, unit_price, stock, product_id,))
            self.cursor.execute(query)
            count = self.cursor.rowcount
            if int(count) > 0:
                return True
            else:
                return False   
        except:
            return False
        
    
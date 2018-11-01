import psycopg2
import re
import os
from psycopg2.extras import RealDictCursor
from flask import current_app as app


class Databasehandler:
    
    def __init__(self):
        
        self.conn =psycopg2.connect(dbname="test_db", user="postgres", host="localhost", password="", port="5433")
        self.cursor=self.conn.cursor()
        self.conn.autocommit = True
        
        
            
        # if app.config.get('ENV') == 'testing':
        #     print(app.config.get('DATABASE_URI'))
            # dbname = app_configuration['testing'].DATABASE
            # self.conn['dbname'] = dbname
        
    # def connect(self):
    
        try:
            
            connection_credentials= """
                    dbname='store_db' user= 'postgres' host='localhost' port='5433'
                    """
            
            connection_credentials1="""
                    dbname='test_db' user= 'postgres' host='localhost' port='5433'
                    """
                # self.conn['dbname'] = dbname
                
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


    # def create_tables(self):
        usercmd="CREATE TABLE IF NOT EXISTS users(user_id SERIAL PRIMARY KEY,username VARCHAR (30),password VARCHAR (10),role BOOLEAN DEFAULT FALSE NOT NULL)"
        self.cursor.execute(usercmd)
    
        pdtcmd="CREATE TABLE IF NOT EXISTS products(product_id SERIAL PRIMARY KEY,product_name VARCHAR(20),unit_price INT, category VARCHAR(15))"
        self.cursor.execute(pdtcmd)
        salecmd="CREATE TABLE IF NOT EXISTS sales(sale_id SERIAL PRIMARY KEY ,entered_by VARCHAR,product_name VARCHAR (20),unit_price INT,quantity INT)"
        self.cursor.execute(salecmd)
        adminuser=f"""
                INSERT INTO users(username, password, role)
                VALUES('admin','admin' ,TRUE)
                """
        self.cursor.execute(adminuser)


    def get_by_argument(self, table, column_name,argument):
        query = "SELECT * FROM {} WHERE {} = '{}';".format(table, column_name, argument)
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result
    def search_user(self,username):
        cmd="SELECT * FROM users WHERE username='{}'".format(username)
        self.cursor.execute(cmd)
        result=self.cursor.fetchone()
        if result:
            return result
        else:
            return {"message":"User doesn't exist"}

    def add_sale(self,entered_by,product_name,unit_price,quantity):
        cmd="INSERT INTO sales(entered_by,product_name,unit_price,quantity) VALUES ('{}','{}','{}','{}');".format(entered_by,product_name,unit_price,quantity)
        
        self.cursor.execute(cmd)

    def add_pdt(self,product_name,unit_price):
        cmd="INSERT INTO products(product_name,unit_price) VALUES ('{}','{}');".format(product_name,unit_price)
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
        cmd="SELECT entered_by,product_name,unit_price,quantity FROM sales WHERE sale_id = {};".format(sale_id) 
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
    
    def get_users(self):
        usercmd ="SELECT * FROM users;"    
        self.cursor.execute(usercmd)
        users = self.cursor.fetchall()
        return users

    def drop_table(self, *table_names):
        for table_name in table_names:
            drop_table = "DROP TABLE IF EXISTS {} CASCADE".format(table_name)
            self.cursor.execute(drop_table)
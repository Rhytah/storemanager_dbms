import psycopg2
import re
import os
from config import app_configuration,Config,DevelopmentConfig,TestingConfig
from smapi import app


dc=DevelopmentConfig()
tc=TestingConfig()
class Databasehandler:
    
    def __init__(self):
        # self.conn =psycopg2.connect(dbname="store_db", user="postgres", host="localhost", password="", port="5433")
        # self.cursor=self.conn.cursor()
        # self.conn.autocommit = True
        
        
            
        # if app.config.get('ENV') == 'testing':
        #     print(app.config.get('DATABASE_URI'))
            # dbname = app_configuration['testing'].DATABASE
            # self.conn['dbname'] = dbname
        

            
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
                self.cursor = self.conn.cursor()
            print("\n\n Database Connected\n\n")
            if app.config.get('ENV') == 'testing':
                print(app.config.get('DATABASE_URI'))
                self.conn = psycopg2.connect(connection_credentials1)
                self.conn.autocommit = True
                self.cursor = self.conn.cursor()
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
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def add_sale(self,entered_by,product_name,unit_price,quantity):
        cmd="INSERT INTO sales(entered_by,product_name,unit_price,quantity) VALUES ('{}','{}','{}','{}');".format(entered_by,product_name,unit_price,quantity)
        self.cursor.execute(cmd)

    def add_pdt(self,product_name,unit_price):
        cmd="INSERT INTO products(product_name,unit_price) VALUES ('{}','{}');".format(product_name,unit_price)
        self.cursor.execute(cmd)


    def get_pdts(self):
        cmd ="SELECT product_id,products FROM products;"
        self.cursor.execute(cmd)
        rows = self.cursor.fetchall()
        self.conn.commit()
        products =[products for products in rows]
        allproducts= []
        for value in range(len(products)):
            product=(
                {'product_id':products[value][0],
                'product':products[value][1]})
            allproducts.append(product)
        return allproducts

    def get_a_pdt(self,product_id):
        cmd="SELECT product_name,unit_price FROM products WHERE product_id = {};".format(product_id) 
        self.cursor.execute(cmd)
        product =self.cursor.fetchone()
        self.conn.commit()
        return product

    def get_sales(self):
        cmd ="SELECT sale_id,sales FROM sales;"
        self.cursor.execute(cmd)
        rows = self.cursor.fetchall()
        self.conn.commit()
        sales =[sales for sales in rows]
        allsale_orders= []
        for value in range(len(sales)):
            sale=(
                {'sale_id':sales[value][0],
                'sale':sales[value][1]})
            allsale_orders.append(sale)
        return allsale_orders

    def get_a_sale(self,sale_id):
        cmd="SELECT entered_by,product_name,unit_price,quantity FROM sales WHERE sale_id = {};".format(sale_id) 
        self.cursor.execute(cmd)
        sale =self.cursor.fetchone()
        self.conn.commit()
        return sale

    def delete_product(self,product_id):
        del_cmd="DELETE FROM products WHERE product_id={}".format(product_id)
        rows_deleted=self.cursor.rowcount
        print(rows_deleted)
        self.cursor.execute(del_cmd)
        self.conn.commit
        return rows_deleted
    
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
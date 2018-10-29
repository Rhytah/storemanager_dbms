import psycopg2

class Databasehandler:
    
    def connect(self):

        try:
            connection_credentials= """
                    dbname='store_db' user= 'postgres' host='localhost' port='5433'
                    """
            self.conn = psycopg2.connect(connection_credentials)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            print("\n\n Database Connected\n\n")
        except Exception as e:
            print(e)
            print("Connection failed")


    def create_tables(self):
        usercmd="CREATE TABLE IF NOT EXISTS users(user_id SERIAL PRIMARY KEY,username VARCHAR (30),password VARCHAR (10),role VARCHAR (10))"
        self.cursor.execute(usercmd)
    
        pdtcmd="CREATE TABLE IF NOT EXISTS products(product_id SERIAL PRIMARY KEY,product_name VARCHAR(20),unit_price INT, category VARCHAR(15))"
        self.cursor.execute(pdtcmd)
        salecmd="CREATE TABLE IF NOT EXISTS sales(sale_id SERIAL PRIMARY KEY ,entered_by VARCHAR,product_name VARCHAR (20),unit_price INT,quantity INT)"
        self.cursor.execute(salecmd)
        adminuser=f"""
                INSERT INTO users(username, password, role)
                VALUES('admin','admin' ,'Owner')
                """
        self.cursor.execute(adminuser)

if __name__ == '__main__':
    db=Databasehandler()
    db.connect()
    db.create_tables()
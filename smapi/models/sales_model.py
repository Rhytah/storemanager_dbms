from smapi.models.dbase import Databasehandler
db=Databasehandler()
class Sale:
    def __init__(self,sale_id,entered_by,product_id,quantity,total):
        self.sale_id= sale_id
        self.entered_by= entered_by
        self.product_id = product_id
        self.quantity = quantity
        self.total = total
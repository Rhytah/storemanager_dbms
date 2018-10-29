
class Sale:
    def __init__(self,sale_id,entered_by,product_name,unit_price,quantity):
        self.sale_id= sale_id
        self.entered_by= entered_by
        self.product_name = product_name
        self.unit_price = unit_price
        self.quantity = quantity



      
        
       

    # def get_sales(self):
    #     if len(self.sale_orders) <1:
    #         return jsonify ({
    #             "message":"No sale orders at the moment"
    #         }),404

    #     if len(self.sale_orders) >1:
    #         return jsonify({
    #             "message":"Fetched Sale orders",
    #             "Sales":self.sale_orders
    #         }),200

    # def fetch_sale(self,saleId):
    #     if len(self.sale_orders)<1:
    #         return jsonify({
    #             "message":"NO sale orders at the moment"
    #         }),404  
        
    #     if len(self.sale_orders)>1:
    #         for a_sale_order in self.sale_orders:
    #             if a_sale_order['saleId']==saleId:
    #                 return jsonify({
    #                     "message":"Fetched sale order",
    #                     "Sale_order":a_sale_order
    #                 }),200
                
    #     return jsonify({"Error":"Order not found , check to see that you wrote the right ID"})

        
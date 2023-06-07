import pandas as pd

class mySGBD():
    def __init__(self) -> None:
        # initialize the tables
        self.prd = pd.read_csv("./actions/products.csv", sep=',')
        self.prd_c = pd.read_csv("./actions/product_colors.csv",sep=',')
        self.prd_s = pd.read_csv("./actions/product_sizes.csv",sep=',')
        
        self.prd['category'] = self.prd['category'].str.lower()
        self.prd['name'] = self.prd['name'].str.lower()
        self.prd_c['color'] = self.prd_c['color'].str.lower()
        self.prd_s['size'] = self.prd_s['size'].str.lower()

        self.allowed_categories = list(self.prd['category'].unique()) # list of the allowed categories
        
        self.allowed_prd_c = None # table of the allowed colors for the chosen category
        self.allowed_colors = [] # list of the allowed colors for the chosen category
        
        self.allowed_prd_s = None # table of the allowed sizes for the chosen color
        self.allowed_sizes = [] # list of the allowed sizes for the chosen color
        
        self.allowed_prd = None # table of the allowed products for the chosen size
        self.allowed_products = [] # list of the allowed products

        self.allowed_quantity = 1 # product quantity in stock
    
    #get available colors for the chosen category
    def get_colors_by_category(self, category):

        self.allowed_prd = self.prd[self.prd['category'].str.lower() == category.lower()]
        products_ids = self.allowed_prd['id'].tolist()

        self.allowed_prd_c = self.prd_c[self.prd_c['product_id'].isin(products_ids)]
        self.allowed_colors = self.allowed_prd_c['color'].unique().tolist()

        return self.allowed_colors

    #get available sizes for the chosen color
    def get_sizes_by_color(self, color):

        self.allowed_prd_c = self.allowed_prd_c[self.allowed_prd_c['color'] == color]
        color_ids = self.allowed_prd_c['id'].tolist()

        self.allowed_prd_s = self.prd_s[self.prd_s['color_id'].isin(color_ids)] 
        self.allowed_sizes = self.allowed_prd_s['size'].unique().tolist()

        return self.allowed_sizes

    #get available product's names for the chosen size
    def get_product_name_by_size(self, size):

        self.allowed_prd_s = self.allowed_prd_s[self.allowed_prd_s['size'].str.lower() == size.lower()]
        products_ids = self.allowed_prd_s['product_id'].tolist()

        self.allowed_prd = self.allowed_prd[self.allowed_prd['id'].isin(products_ids)]
        self.allowed_products = self.allowed_prd['name'].tolist()

        return self.allowed_products
    
    #get available product's quantity for the chosen product name
    def get_product_quantity_by_size(self):

        self.allowed_quantity = self.allowed_prd_s['size_quantity'].tolist()[0]

        return self.allowed_quantity
    
    #update the quantity of the ordered product
    def update_quantity(self, ordered_quantity):

        allowed_prd_s_list = self.allowed_prd_s.values.flatten().tolist()
        product_id = allowed_prd_s_list[1]
        color_id = allowed_prd_s_list[2]
        size = allowed_prd_s_list[3]

        ordered_quantity = int(ordered_quantity)
        
        self.prd_s.loc[(self.prd_s['product_id'] == product_id) & (self.prd_s['color_id'] == color_id) & (self.prd_s['size'].str.lower() == size), 'size_quantity'] -= ordered_quantity
        self.prd_s = self.prd_s[self.prd_s['size_quantity'] > 0]
        
        self.prd_c.loc[(self.prd_c['product_id'] == product_id) & (self.prd_c['id'] == color_id), 'color_quantity'] -= ordered_quantity
        self.prd_c = self.prd_c[self.prd_c['color_quantity'] > 0]

        self.prd.loc[self.prd['id'] == product_id, 'quantity'] -= ordered_quantity
        self.prd = self.prd[self.prd['quantity'] > 0]



    
if __name__ == '__main__':

    #code to test the functions
    # sgbd = mySGBD()
    # categories = sgbd.allowed_categories
    # print(categories)

    # colors = sgbd.get_colors_by_category('jeans')
    # print(sgbd.allowed_prd)
    # print(colors)

    # sizes = sgbd.get_sizes_by_color('blue')
    # print(sgbd.allowed_prd_c)
    # print(sgbd.allowed_prd_s)
    # print(sizes)

    # products = sgbd.get_product_name_by_size('l')
    # print(products) 
    # print(sgbd.allowed_prd_s)

    # quantities = sgbd.get_product_quantity_by_size()
    # print(quantities)
    
    pass
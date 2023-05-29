import pandas as pd
import csv
df = pd.read_csv("./actions/products.csv", sep='|')
pc = pd.read_csv("./actions/product_color.csv",sep=',')
ps = pd.read_csv("./actions/product_size.csv",sep=',')
ALLOWED_PRODUCT_CATEGORIES = list(df['category'].unique())
Allowed_product_Colors=list(pc['color'].unique())
Allowed_product_sizes=list(ps['size'].unique())


#get available colors for the chosen category
def get_color_by_category(category):
    df = pd.read_csv("./actions/products.csv", sep='|')
    filtered_df = df[df['category'].str.lower() == category.lower()]
    product_ids = filtered_df['id'].tolist()

    pc = pd.read_csv("./actions/product_color.csv", sep=',')
    filtered_pc = pc[pc['product_id'].isin(product_ids)]
    color = filtered_pc['color'].unique().tolist()

    return color

#get available sizes for the chosen category and color
def get_size_by_color(color,category):
    df = pd.read_csv("./actions/products.csv", sep='|')
    filtered_df = df[df['category'].str.lower() == category.lower()]
    product_ids = filtered_df['id'].tolist()

    pc = pd.read_csv("./actions/product_color.csv", sep=',')
    filtered_pc = pc[pc['product_id'].isin(product_ids)]
    color_ids= filtered_pc['id'].tolist()


    ps = pd.read_csv("./actions/product_size.csv", sep=',')
    filtered_ps = ps[ps['color_id'].isin(color_ids)] 
    size = filtered_ps['size'].unique().tolist()

    return size





#get available product's names for the chosen category and color and size
def get_product_name(category, color, size):
    df = pd.read_csv("./actions/products.csv", sep='|')
    filtered_df = df[df['category'].str.lower() == category.lower()]
    product_ids = filtered_df['id'].tolist()

    pc = pd.read_csv("./actions/product_color.csv", sep=',')
    filtered_pc = pc[pc['product_id'].isin(product_ids)]
    color_ids = filtered_pc[filtered_pc['color'].str.lower() == color.lower()]['id'].tolist()

    ps = pd.read_csv("./actions/product_size.csv", sep=',')
    filtered_ps = ps[(ps['color_id'].isin(color_ids)) & (ps['size'].str.lower() == size.lower())]
    product_ids = filtered_ps['product_id'].tolist()

    filtered_products = df[df['id'].isin(product_ids)]
    product_names = filtered_products['name'].tolist()

    return product_names

 
#get available product's quantity for the chosen  color and size and product name
def get_product_quantity_by_size(color, size, name):
    df = pd.read_csv("./actions/products.csv", sep='|')
    filtered_df = df[df['name'].str.lower() == name.lower()]
    product_id = filtered_df['id'].tolist()

    pc = pd.read_csv("./actions/product_color.csv", sep=',')
    filtered_pc = pc[pc['product_id'].isin(product_id)]
    color_ids = filtered_pc[filtered_pc['color'].str.lower() == color.lower()]['id'].tolist()

    ps = pd.read_csv("./actions/product_size.csv", sep=',')
    filtered_ps = ps[(ps['color_id'].isin(color_ids)) & (ps['size'].str.lower() == size.lower()) & (ps['product_id'].isin(product_id))]
    product_quantity = filtered_ps['size_quantity'].tolist()

    return product_quantity






   









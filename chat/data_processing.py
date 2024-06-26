import pandas as pd
import settings as s

def generate_text_from_data(df):
    """
    Generates a list of descriptive texts based on the product data in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing product data.

    Returns:
        list: A list of strings, each containing a descriptive text about a product or statistical insight.
    """

    df['availability'] = df['availability'].map(s.availability_map)
    df['item_condition'] = df['item_condition'].map(s.condition_map)
    
    df['product_type'] = df['product_type'].str.lower()

    text_blocks = []

    operations = [
        lambda row: f"{row['title']} by {row['brand']} in {row['product_type']} condition is sold at {row['price']} {row['currency']}. Check it out on our site: {row['url']}",
        lambda row: f"Looking for {row['title']}? We offer it in {row['item_condition']} condition. It is {row['availability']}.",
        lambda row: f"Explore our collection of {row['category']} products including {row['title']} in the {row['sub_cateory']} subcategory.",
        lambda row: f"Read more about {row['title']}: {row['description']} For full product details, visit {row['url']}",
        lambda row: f"{row['title']} has an average rating of {row['average_rating']} from over {row['reviews_count']} reviews!",
        lambda row: f"Stay informed with the latest price and availability of {row['title']} on our website at {row['url']}. Currently {row['availability']}",
        lambda row: f"Rated {row['content_rating']}, {row['title']} is ideal for customers looking for products in the {row['category']} category."
    ]
    
    for operation in operations:
        text_blocks.extend(df.apply(operation, axis=1).tolist())

    average_prices = df.groupby('category')['price'].mean().reset_index()
    for _, row in average_prices.iterrows():
        text_blocks.append(f"The average price for {row['category']} products is approximately {row['price']:.2f} {df['currency'].iloc[0]}.")

    df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce')
    top_rated = df.loc[df.groupby('category')['average_rating'].idxmax()]
    for _, row in top_rated.iterrows():
        text_blocks.append(f"The highest-rated product in the {row['category']} category is {row['title']} with a rating of {row['average_rating']} stars.")
    
    return text_blocks

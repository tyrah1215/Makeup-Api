import requests
import pandas as pd

# Fetch data from API
def fetch_data(product_type):
    """Fetch data from the API for a given product type."""
    url = f'http://makeup-api.herokuapp.com/api/v1/products.json?product_type={product_type}'
    response = requests.get(url)
    
    # Ensure connected to API (200 status code)
    if response.status_code == 200:
        print(f"Successfully fetched data for {product_type}.")
    else:
        print(f"Failed to fetch data for {product_type}.")
    
    return response.json()

def get_products(products):
    """Function to filter and return product data."""
    filtered_products = []
    for product in products:
        name = product.get('name')
        brand = product.get('brand')
        price = product.get('price')
        rating = product.get('rating')

        # Make sure price and rating are valid numbers
        try:
            if price is not None and rating is not None:
                price = float(price)  # Convert price to float
                rating = float(rating)  # Convert rating to float
                filtered_products.append({
                    'name': name,
                    'brand': brand,
                    'price': price,
                    'rating': rating
                })
        except (ValueError, TypeError):
            # Skip the product if price or rating not valid
            continue

    return filtered_products

def get_average(filtered_products):
    """Calculate the average price of the given products."""
    if not filtered_products:
        return 0
    total_sum = sum(product['price'] for product in filtered_products)
    count = len(filtered_products)
    return total_sum / count

def low_end_products(filtered_products):
    """Function to get products under the average price."""
    average_price = get_average(filtered_products)
    return [product for product in filtered_products if product['price'] < average_price]

def high_end_products(filtered_products):
    """Function to get products over the average price."""
    average_price = get_average(filtered_products)
    return [product for product in filtered_products if product['price'] > average_price]

def print_products(products, category):
    """Helper function to print products in a formatted table."""
    if not products:
        print(f"\nNo {category} products available.")
        return
    df = pd.DataFrame(products)
    print(f"\n{category} Products:")
    print(df.to_string(index=False))

def compare_products(low_end, high_end, category):
    """Compare and display products side by side."""
    df_low_end = pd.DataFrame(low_end)
    df_high_end = pd.DataFrame(high_end)

    # Display the data side by side
    comparison_df = pd.concat([df_low_end, df_high_end], axis=1, keys=[f"---{category} Low-End---", f"---{category} High-End---"])
    print(f"\n{category} Comparison (Low-End vs High-End):")
    print(comparison_df)

def process_product_type(product_type):
    """Fetch, filter, and compare products of a given type."""
    products = fetch_data(product_type)
    filtered_products = get_products(products)
    
    # Print the avg price before the comparison tables
    average_price = get_average(filtered_products)
    print(f"\nThe average price for {product_type} is: ${average_price:.2f}")

    low_end = low_end_products(filtered_products)
    high_end = high_end_products(filtered_products)

    compare_products(low_end, high_end, product_type.capitalize())

if __name__ == "__main__":
    product_types = [
        'blush', 'bronzer', 'eyeliner', 'eyebrow', 'eyeshadow', 'foundation',
        'lipstick', 'lip_liner',  'mascara'
    ]
    
    for product_type in product_types:
        process_product_type(product_type)
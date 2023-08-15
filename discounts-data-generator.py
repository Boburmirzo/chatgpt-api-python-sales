import pandas as pd
import random
from datetime import datetime, timedelta

# List of example values
countries = ['USA']
cities = ['New York', 'Los Angeles', 'San Francisco']
states = ['NY', 'CA', 'IL']
regions = ['East', 'West', 'Central', 'South']
categories = ['Footwear']
sub_categories = ['Men Shoes', 'Women Shoes']
brands = ['Nike', 'Addidas', "Reebok", "Puma"]
product_names = ['Running Shoes', 'Casual Shoes', 'Formal Shoes']
currencies = ['USD', 'EUR', 'GBP']
addresses = ['123 Main St', '456 Market St', '789 Elm St', '321 Oak St', '100 Pine St']

# Generate dataset
data = []
for i in range(10):
    discount_until = (datetime.now() + timedelta(days=random.randint(0, 364))).strftime('%Y-%m-%d')
    country = random.choice(countries)
    city = random.choice(cities)
    state = random.choice(states)
    postal_code = str(random.randint(10000, 99999))
    region = random.choice(regions)
    product_id = str(random.randint(1000, 9999))
    category = random.choice(categories)
    sub_category = random.choice(sub_categories)
    brand = random.choice(brands)
    product_name = random.choice(product_names)
    currency = random.choice(currencies)
    actual_price = round(random.uniform(50, 200), 2)
    discount_percentage = random.randint(5, 30)
    discount_price = round(actual_price * (1 - discount_percentage / 100), 2)
    address = random.choice(addresses)

    row = [discount_until, country, city, state, postal_code, region, product_id, category, sub_category, brand, product_name, currency, actual_price, discount_price, discount_percentage, address]
    data.append(row)

# Create DataFrame
df = pd.DataFrame(data, columns=["discount_until", "country", "city", "state", "postal_code", "region", "product_id", "category", "sub_category", "brand", "product_name", "currency", "actual_price", "discount_price", "discount_percentage", "address"])

# Save to CSV
df.to_csv('./data/csv/discounts.csv', index=False)

print('Dataset generated and saved to future_discounts.csv')
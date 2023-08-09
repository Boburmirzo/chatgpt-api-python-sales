import pathway as pw

def concat_with_titles(*args) -> str:
    titles = [
        "country",
        "city",
        "discount_until",
        "state",
        "product_id",
        "postal_code",
        "region",
        "category",
        "sub_category",
        "brand",
        "product_name",
        "actual_price",
        "discount_price",
        "discount_percentage",
        "address",
        "currency",
        "ship_date",
    ]
    combined = [f"{title}: {value}" for title, value in zip(titles, args)]
    return ', '.join(combined)

def transform_data(sales_data):
    combined_data = sales_data.select(
        doc=pw.apply(concat_with_titles,
                     pw.this.country,
                     pw.this.city,
                     pw.this.discount_until,
                     pw.this.state,
                     pw.this.product_id,
                     pw.this.postal_code,
                     pw.this.region,
                     pw.this.category,
                     pw.this.sub_category,
                     pw.this.brand,
                     pw.this.product_name,
                     pw.this.actual_price,
                     pw.this.discount_price,
                     pw.this.discount_percentage,
                     pw.this.address,
                     pw.this.currency),
    )
    return combined_data

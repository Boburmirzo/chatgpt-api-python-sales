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


def transform(sales_data):
    return sales_data.select(
        doc=pw.apply(concat_with_titles,
                     sales_data.country,
                     sales_data.city,
                     sales_data.discount_until,
                     sales_data.state,
                     sales_data.product_id,
                     sales_data.postal_code,
                     sales_data.region,
                     sales_data.category,
                     sales_data.sub_category,
                     sales_data.brand,
                     sales_data.product_name,
                     sales_data.actual_price,
                     sales_data.discount_price,
                     sales_data.discount_percentage,
                     sales_data.address,
                     sales_data.currency),
    )

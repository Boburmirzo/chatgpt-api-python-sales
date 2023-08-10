import pathway as pw


# Maps each data row into a structured document schema using Pathway
class DiscountsInputSchema(pw.Schema):
    discount_until: str
    country: str
    city: str
    state: str
    postal_code: str
    region: str
    product_id: str
    category: str
    sub_category: str
    brand: str
    product_name: str
    currency: str
    actual_price: str
    discount_price: str
    discount_percentage: str
    address: str


class QueryInputSchema(pw.Schema):
    query: str
    user: str

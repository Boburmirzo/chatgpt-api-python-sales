import pathway as pw


# Maps each data row into a structured document schema using Pathway
class CsvDiscountsInputSchema(pw.Schema):
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


class RainforestDealsInputSchema(pw.Schema):
    position: int
    link: str
    asin: str
    is_lightning_deal: bool
    deal_type: str
    is_prime_exclusive: bool
    starts_at: str
    ends_at: str
    type: str
    title: str
    image: str
    deal_price: float
    old_price: float
    currency: str
    merchant_name: str
    free_shipping: bool
    is_prime: bool
    is_map: bool
    deal_id: str
    seller_id: str
    description: str
    rating: float
    ratings_total: int

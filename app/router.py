
from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

faq = Route(
    name="faq",
    utterances=[
        "What is your return policy?",
        "How can I return a product?",
        "Can I return a damaged product?",
        "What if I receive a defective item?",
        "Can I pay by COD?",
        "Do you have COD?","Is cash on delivery available?",
        "Can I get a refund?",
        "How long does a refund take?",
        "How can I cancel my order?",
        "Can I cancel an order after placing it?",
        "How long does shipping take?",
        "Do you offer free shipping?",'what are the payment options you accept?','what all are the payment methods you provide?'
    ]
)
sql=Route(name='sql',utterances=[
    "Show me all products",
    "What products are available?",
    "Show me products under 2000 rupees",
    "Show me products above 5000 rupees",
    "Which products are between 1000 and 3000?",
    "Find products priced between 2000 and 5000",
    "Show me products with a rating above 4",
    "Which products have a rating greater than 4.5?",
    "Find products with ratings below 3",
    "Show me the highest rated products",
    "Which products have the best ratings?",
    "Show me products with more than 100 ratings",
    "Which products have the most reviews?",
    "Show me Nike products",
    "Find all Adidas products",
    "What products are from Sparx?",
    "Show me products from Puma",
    "Find Nike shoes under 3000",
    "Show me Adidas products with a rating above 4",
    "Find products with a discount greater than 20%",
    "Which products have more than 30% discount?",
    "Show me products with discounts between 10% and 30%",
    "Which is the cheapest product?",
    "Which is the most expensive product?",
    "What is the average product price?",
    "How many products are available?",
    "How many products cost less than 2000?",
    "How many products have a rating above 4.5?",
    "What is the highest rated product?",
    "What is the cheapest Nike product?",
    "What is the most expensive Adidas product?",
    "Show me the top 5 highest rated products",
    "Show me the 10 cheapest products",
    "Show me products sorted by price",
    "Sort products by rating",
    "Show me products with the highest discounts",
    "Find shoes between 1000 and 2000 rupees",
    "Find running shoes with a rating above 4",
    "Show me products from Nike priced below 3000",
    "Which Nike products have a discount above 10%?"
       ])

route = SemanticRouter(
    routes=[faq,sql],
    encoder=HuggingFaceEncoder(model_name='all-MiniLM-L6-v2'),auto_sync='local')

result = route(text='how many orders were placed last month?')

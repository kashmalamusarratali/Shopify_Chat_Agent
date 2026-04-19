import os
import requests
from dotenv import load_dotenv

load_dotenv()

STORE = os.getenv("SHOPIFY_STORE")
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

def get_order_status(order_number: str):
    url = f"https://{STORE}.myshopify.com/admin/api/2023-10/orders.json?name={order_number}"

    headers = {
        "X-Shopify-Access-Token": TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if "orders" in data and len(data["orders"]) > 0:
        order = data["orders"][0]
        return f"Order {order_number} is {order['financial_status']} and fulfillment status is {order['fulfillment_status']}"
    else:
        return "Order not found."
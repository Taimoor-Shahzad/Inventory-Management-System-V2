import json
from typing import List
from authentication import AuthenticationManager, AuthorizationError, AuthenticationError, Role

# Paths to Data Files
INVENTORY_FILE = "data/inventory.json"

# Custom Exceptions
class ProductNotFoundError(Exception):
    pass

class InsufficientStockError(Exception):
    pass

# Product Management
class Product:
    def __init__(self, product_id: int, name: str, category: str, price: float, stock_quantity: int):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

class ProductManager:
    def __init__(self):
        self.products = self.load_inventory()

    def load_inventory(self) -> List[Product]:
        try:
            with open(INVENTORY_FILE, "r") as f:
                data = json.load(f)
            return [
                Product(
                    product["product_id"],
                    product["name"],
                    product["category"],
                    product["price"],
                    product["stock_quantity"],
                )
                for product in data
            ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_inventory(self):
        with open(INVENTORY_FILE, "w") as f:
            json.dump(
                [
                    {
                        "product_id": product.product_id,
                        "name": product.name,
                        "category": product.category,
                        "price": product.price,
                        "stock_quantity": product.stock_quantity,
                    }
                    for product in self.products
                ],
                f,
            )

    def add_product(self, product: Product):
        if any(p.product_id == product.product_id for p in self.products):
            raise ValueError("Product with this ID already exists.")
        self.products.append(product)
        self.save_inventory()

    def remove_product(self, product_id: int):
        self.products = [p for p in self.products if p.product_id != product_id]
        self.save_inventory()

    def get_products(self) -> List[Product]:
        return self.products

    def adjust_stock(self, product_id: int, quantity: int):
        for product in self.products:
            if product.product_id == product_id:
                if product.stock_quantity + quantity < 0:
                    raise InsufficientStockError("Cannot reduce stock below zero.")
                product.stock_quantity += quantity
                self.save_inventory()
                return
        raise ProductNotFoundError("Product not found.")

# Initialize Authentication Manager for Consistency
auth_manager = AuthenticationManager()

# Usage Example
if __name__ == "__main__":
    product_manager = ProductManager()

    # Add default admin user if not already present
    try:
        auth_manager.register_user("admin", "adminpass", Role.ADMIN)
        print("Default admin user added.")
    except ValueError:
        print("Admin user already exists.")

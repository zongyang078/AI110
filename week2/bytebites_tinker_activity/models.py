# ByteBites Backend Models
# Classes: Customer, MenuItem, Menu, Order

class Customer:
    def __init__(self, name: str):
        self.name = name
        self.purchase_history = []

    def verify_user(self) -> bool:
        return len(self.purchase_history) > 0


class MenuItem:
    def __init__(self, name: str, price: float, category: str, popularity: float):
        self.name = name
        self.price = price
        self.category = category
        self.popularity = popularity


class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, item: MenuItem):
        self.items.append(item)

    def filter_by_category(self, category: str) -> list:
        return [item for item in self.items if item.category == category]

    def sort_by_popularity(self) -> list:
        return sorted(self.items, key=lambda item: item.popularity, reverse=True)


class Order:
    def __init__(self, customer: Customer):
        self.customer = customer
        self.items = []

    def add_item(self, item: MenuItem):
        self.items.append(item)

    def calculate_total(self) -> float:
        return sum(item.price for item in self.items)
from models import Customer, MenuItem, Menu, Order


def test_order_total_with_multiple_items():
    customer = Customer("Zoe")
    order = Order(customer)
    order.add_item(MenuItem("Burger", 8.99, "Entrees", 4.5))
    order.add_item(MenuItem("Soda", 2.49, "Drinks", 3.8))
    assert round(order.calculate_total(), 2) == 11.48


def test_order_total_is_zero_when_empty():
    customer = Customer("Zoe")
    order = Order(customer)
    assert order.calculate_total() == 0


def test_filter_by_category():
    menu = Menu()
    menu.add_item(MenuItem("Soda", 2.49, "Drinks", 3.8))
    menu.add_item(MenuItem("Water", 1.00, "Drinks", 3.0))
    menu.add_item(MenuItem("Burger", 8.99, "Entrees", 4.5))
    drinks = menu.filter_by_category("Drinks")
    assert len(drinks) == 2
    assert all(item.category == "Drinks" for item in drinks)


def test_filter_by_category_no_match():
    menu = Menu()
    menu.add_item(MenuItem("Burger", 8.99, "Entrees", 4.5))
    result = menu.filter_by_category("Desserts")
    assert len(result) == 0


def test_sort_by_popularity():
    menu = Menu()
    menu.add_item(MenuItem("Soda", 2.49, "Drinks", 3.8))
    menu.add_item(MenuItem("Cake", 5.99, "Desserts", 4.7))
    menu.add_item(MenuItem("Burger", 8.99, "Entrees", 4.5))
    sorted_items = menu.sort_by_popularity()
    assert sorted_items[0].name == "Cake"
    assert sorted_items[-1].name == "Soda"


def test_verify_user():
    customer = Customer("Zoe")
    assert customer.verify_user() == False
    customer.purchase_history.append("some_order")
    assert customer.verify_user() == True
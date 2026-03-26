from models import Customer, MenuItem, Menu, Order

# --- Create menu items ---
burger = MenuItem("Spicy Burger", 8.99, "Entrees", 4.5)
soda = MenuItem("Large Soda", 2.49, "Drinks", 3.8)
cake = MenuItem("Chocolate Cake", 5.99, "Desserts", 4.7)
water = MenuItem("Water", 1.00, "Drinks", 3.0)
fries = MenuItem("Fries", 3.49, "Entrees", 4.2)

# --- Build the menu ---
menu = Menu()
for item in [burger, soda, cake, water, fries]:
    menu.add_item(item)

# --- Test filter by category ---
drinks = menu.filter_by_category("Drinks")
print("=== Drinks ===")
for d in drinks:
    print(f"  {d.name} - ${d.price}")

# --- Test sort by popularity ---
popular = menu.sort_by_popularity()
print("\n=== Sorted by Popularity ===")
for p in popular:
    print(f"  {p.name} (rating: {p.popularity})")

# --- Test order and total ---
customer = Customer("Zoe")
order = Order(customer)
order.add_item(burger)
order.add_item(soda)
order.add_item(cake)
print(f"\n=== Order for {order.customer.name} ===")
for item in order.items:
    print(f"  {item.name} - ${item.price}")
print(f"  Total: ${order.calculate_total():.2f}")

# --- Test verify user ---
print(f"\n=== Verify User ===")
print(f"  Before purchase: {customer.verify_user()}")
customer.purchase_history.append(order)
print(f"  After purchase: {customer.verify_user()}")
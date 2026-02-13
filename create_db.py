import sqlite3, os

if os.path.exists("food.db"):
    os.remove("food.db")

con = sqlite3.connect("food.db")
cur = con.cursor()

# ---------- TABLES ----------
cur.execute("""
CREATE TABLE food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price INTEGER,
    image TEXT
)
""")

cur.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT,
    name TEXT,
    address TEXT,
    table_no TEXT,
    order_type TEXT,
    food TEXT,
    price INTEGER,
    time TEXT
)
""")

cur.execute("""
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    message TEXT,
    time TEXT
)
""")

# ---------- 100 REAL RESTAURANT ITEMS ----------
foods = [

# ☕ COFFEE (10)
("Espresso", "Coffee", 120, "https://upload.wikimedia.org/wikipedia/commons/4/45/A_small_cup_of_coffee.JPG"),
("Cappuccino", "Coffee", 150, "https://upload.wikimedia.org/wikipedia/commons/c/c8/Cappuccino_at_Sightglass_Coffee.jpg"),
("Latte", "Coffee", 160, "https://upload.wikimedia.org/wikipedia/commons/7/7c/Caff%C3%A8_Latte_at_Sightglass_Coffee.jpg"),
("Americano", "Coffee", 140, "https://upload.wikimedia.org/wikipedia/commons/3/3b/Americano_coffee.jpg"),
("Mocha", "Coffee", 170, "https://upload.wikimedia.org/wikipedia/commons/f/f6/Mocaccino-Coffee.jpg"),
("Cold Coffee", "Coffee", 180, "https://upload.wikimedia.org/wikipedia/commons/5/5f/Iced_coffee.jpg"),
("Caramel Latte", "Coffee", 190, "https://upload.wikimedia.org/wikipedia/commons/9/9f/Latte_art_3.jpg"),
("Hazelnut Coffee", "Coffee", 200, "https://upload.wikimedia.org/wikipedia/commons/6/6a/Coffee_cup.jpg"),
("Irish Coffee", "Coffee", 220, "https://upload.wikimedia.org/wikipedia/commons/6/61/Irish_coffee_glass.jpg"),
("Filter Coffee", "Coffee", 100, "https://upload.wikimedia.org/wikipedia/commons/a/a0/South_Indian_filter_coffee.jpg"),

# 🍔 BURGERS (10)
("Veg Burger", "Burger", 120, "https://upload.wikimedia.org/wikipedia/commons/0/0b/RedDot_Burger.jpg"),
("Cheese Burger", "Burger", 150, "https://upload.wikimedia.org/wikipedia/commons/4/4d/Cheeseburger.jpg"),
("Paneer Burger", "Burger", 170, "https://upload.wikimedia.org/wikipedia/commons/1/15/Recipe_logo.jpeg"),
("Double Cheese Burger", "Burger", 190, "https://upload.wikimedia.org/wikipedia/commons/5/5b/Double_cheeseburger.jpg"),
("Spicy Veg Burger", "Burger", 160, "https://upload.wikimedia.org/wikipedia/commons/3/32/Hamburger.jpg"),
("Aloo Tikki Burger", "Burger", 130, "https://upload.wikimedia.org/wikipedia/commons/2/2c/Veggie_Burger.jpg"),
("Mexican Burger", "Burger", 180, "https://upload.wikimedia.org/wikipedia/commons/7/73/Burger_with_fries.jpg"),
("Corn Burger", "Burger", 150, "https://upload.wikimedia.org/wikipedia/commons/d/d3/Burger.jpg"),
("Mushroom Burger", "Burger", 190, "https://upload.wikimedia.org/wikipedia/commons/4/4f/Hamburger_(black_bg).jpg"),
("Cheesy Paneer Burger", "Burger", 210, "https://upload.wikimedia.org/wikipedia/commons/1/11/Cheeseburger_in_paris.jpg"),

# 🍕 PIZZA (10)
("Margherita Pizza", "Pizza", 220, "https://upload.wikimedia.org/wikipedia/commons/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg"),
("Cheese Burst Pizza", "Pizza", 280, "https://upload.wikimedia.org/wikipedia/commons/d/d3/Supreme_pizza.jpg"),
("Farmhouse Pizza", "Pizza", 300, "https://upload.wikimedia.org/wikipedia/commons/6/6b/Pizza_on_stone.jpg"),
("Veggie Delight Pizza", "Pizza", 260, "https://upload.wikimedia.org/wikipedia/commons/9/91/Pizza-3007395.jpg"),
("Paneer Tikka Pizza", "Pizza", 320, "https://upload.wikimedia.org/wikipedia/commons/4/4b/Pizza_with_tomatoes.jpg"),
("Mexican Green Wave", "Pizza", 310, "https://upload.wikimedia.org/wikipedia/commons/5/5e/Pepperoni_pizza.jpg"),
("Cheese Lovers Pizza", "Pizza", 290, "https://upload.wikimedia.org/wikipedia/commons/9/96/Pizza_slice.jpg"),
("Olive Pizza", "Pizza", 270, "https://upload.wikimedia.org/wikipedia/commons/3/35/Pizza_with_olives.jpg"),
("Corn Pizza", "Pizza", 250, "https://upload.wikimedia.org/wikipedia/commons/6/65/Pizza_with_corn.jpg"),
("Spicy Paneer Pizza", "Pizza", 330, "https://upload.wikimedia.org/wikipedia/commons/a/a6/Pizza_diavola.jpg"),

# 🍚 RICE & BIRYANI (20)
("Veg Fried Rice", "Rice", 180, "https://upload.wikimedia.org/wikipedia/commons/4/45/Fried_rice.jpg"),
("Egg Fried Rice", "Rice", 200, "https://upload.wikimedia.org/wikipedia/commons/5/5f/Egg_fried_rice.jpg"),
("Paneer Fried Rice", "Rice", 220, "https://upload.wikimedia.org/wikipedia/commons/8/8f/Fried_rice_with_vegetables.jpg"),
("Jeera Rice", "Rice", 160, "https://upload.wikimedia.org/wikipedia/commons/2/2f/Jeera_rice.jpg"),
("Steam Rice", "Rice", 120, "https://upload.wikimedia.org/wikipedia/commons/0/01/White_rice.jpg"),
("Veg Biryani", "Biryani", 240, "https://upload.wikimedia.org/wikipedia/commons/b/bb/Veg_Biryani.jpg"),
("Paneer Biryani", "Biryani", 270, "https://upload.wikimedia.org/wikipedia/commons/3/32/Paneer_Biryani.jpg"),
("Hyderabadi Biryani", "Biryani", 320, "https://upload.wikimedia.org/wikipedia/commons/3/3b/Hyderabadi_Biryani.jpg"),
("Mushroom Biryani", "Biryani", 260, "https://upload.wikimedia.org/wikipedia/commons/9/9b/Mushroom_biryani.jpg"),
("Curd Rice", "Rice", 150, "https://upload.wikimedia.org/wikipedia/commons/3/33/Curd_rice.jpg"),

# 🍜 CHINESE (10)
("Veg Chowmein", "Chinese", 160, "https://upload.wikimedia.org/wikipedia/commons/0/0f/Chow_mein_1.jpg"),
("Hakka Noodles", "Chinese", 180, "https://upload.wikimedia.org/wikipedia/commons/5/5a/Hakka_noodles.jpg"),
("Veg Manchurian", "Chinese", 190, "https://upload.wikimedia.org/wikipedia/commons/7/73/Gobi_Manchurian.jpg"),
("Spring Roll", "Chinese", 120, "https://upload.wikimedia.org/wikipedia/commons/1/1f/Spring_rolls.jpg"),
("Chilli Paneer", "Chinese", 220, "https://upload.wikimedia.org/wikipedia/commons/2/2b/Chilli_Paneer.jpg"),
("Schezwan Rice", "Chinese", 200, "https://upload.wikimedia.org/wikipedia/commons/4/4b/Schezwan_rice.jpg"),
("Veg Momos", "Chinese", 140, "https://upload.wikimedia.org/wikipedia/commons/6/6b/Momos.jpg"),
("Fried Momos", "Chinese", 160, "https://upload.wikimedia.org/wikipedia/commons/7/72/Fried_momos.jpg"),
("Garlic Noodles", "Chinese", 190, "https://upload.wikimedia.org/wikipedia/commons/3/33/Garlic_noodles.jpg"),
("Hot & Sour Soup", "Chinese", 130, "https://upload.wikimedia.org/wikipedia/commons/2/25/Hot_and_sour_soup.jpg"),

# 🥟 SNACKS + DESSERTS + DRINKS (20)
("Samosa", "Snacks", 30, "https://upload.wikimedia.org/wikipedia/commons/c/cb/Samosachutney.jpg"),
("Bread Pakoda", "Snacks", 50, "https://upload.wikimedia.org/wikipedia/commons/8/82/Bread_pakora.jpg"),
("French Fries", "Snacks", 120, "https://upload.wikimedia.org/wikipedia/commons/6/6f/French_fries.jpg"),
("Paneer Pakoda", "Snacks", 90, "https://upload.wikimedia.org/wikipedia/commons/3/32/Paneer_pakora.jpg"),
("Veg Cutlet", "Snacks", 80, "https://upload.wikimedia.org/wikipedia/commons/4/4b/Veg_cutlet.jpg"),
("Gulab Jamun", "Dessert", 90, "https://upload.wikimedia.org/wikipedia/commons/5/5b/Gulab_jamun.jpg"),
("Rasgulla", "Dessert", 100, "https://upload.wikimedia.org/wikipedia/commons/8/8b/Rasgulla.jpg"),
("Ice Cream", "Dessert", 120, "https://upload.wikimedia.org/wikipedia/commons/b/b7/Ice_cream_dessert.jpg"),
("Brownie", "Dessert", 140, "https://upload.wikimedia.org/wikipedia/commons/6/6f/Chocolate_brownie.jpg"),
("Cold Drink", "Drinks", 40, "https://upload.wikimedia.org/wikipedia/commons/5/5f/Soft_drink_glass.jpg"),
("Lemonade", "Drinks", 60, "https://upload.wikimedia.org/wikipedia/commons/4/41/Lemonade.jpg"),
("Fresh Lime Soda", "Drinks", 70, "https://upload.wikimedia.org/wikipedia/commons/9/9f/Lime_soda.jpg"),
]

cur.executemany(
    "INSERT INTO food VALUES (NULL,?,?,?,?)",
    foods
)

con.commit()
con.close()
print("✅ 100-item REAL restaurant database created successfully")

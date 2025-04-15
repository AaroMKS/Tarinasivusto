import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM items")
db.execute("DELETE FROM reviews")

user_count = 100
items_count = 10**5
reviews_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, items_count + 1):
    user_id=random.randint(1, user_count)
    db.execute("INSERT INTO items (title, user_id) VALUES (?, ?)",
               ["items" + str(i), user_id])

for i in range(1, reviews_count + 1):
    user_id = random.randint(1, user_count)
    items_id = random.randint(1, items_count)
    grade=random.randint(1, 10)
    db.execute("""INSERT INTO reviews (grade, review, user_id, item_id)
                VALUES (?, ?, ?, ?)""",
                [grade, "reviews" + str(i), user_id, items_id])

db.commit()
db.close()
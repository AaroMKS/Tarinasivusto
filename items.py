import db
def add_item(title, description, story, user_id):
    sql = "INSERT INTO items (title, description, story, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, story, user_id])
def get_items():
    sql="SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql= """SELECT items.id, items.title, items.description, items.story, users.id user_id, users.username FROM items, users WHERE items.user_id = users.id AND items.id=?"""
    return db.query(sql, [item_id])[0]

def update_item(item_id, title, description, story):
    sql= """UPDATE items SET title = ?, description = ?, story = ? WHERE id = ?"""
    db.execute(sql, [title, description, story, item_id])
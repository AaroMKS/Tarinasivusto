import db
def add_item(title, description, story, user_id):
    sql = "INSERT INTO items (title, description, story, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, story, user_id])
import db
def get_all_classes():
    sql="SELECT title, value FROM classes ORDER BY id"
    result=db.query(sql)
    classes={}
    for title, value in result:
        classes[title]=[]
    for title, value in result:
        classes[title].append(value)
    return classes


def add_item(title, description, story, user_id, classes):
    sql = "INSERT INTO items (title, description, story, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, story, user_id])

    item_id=db.last_insert_id()

    sql="INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def add_review(item_id, user_id, grade, review):
    sql = "INSERT INTO reviews (item_id, user_id, grade, review) VALUES (?, ?, ?, ?)"
    db.execute(sql, [item_id, user_id, grade, review])

def get_reviews(item_id):
    sql = """SELECT reviews.grade, reviews.review, users.id user_id, users.username 
            FROM reviews, users
            WHERE reviews.item_id=? AND reviews.user_id = users.id
            ORDER BY reviews.id DESC"""
    return db.query(sql, [item_id])


def get_classes(item_id):
    sql="SELECT title, value FROM item_classes WHERE item_id=?"
    return db.query(sql, [item_id])
def get_items():
    sql="""SELECT items.id, items.title, users.id user_id, users.username, COALESCE(SUM(reviews.grade)/COUNT(reviews.id), '-') review_average 
    FROM items JOIN users ON items.user_id=users.id LEFT JOIN reviews on items.id=reviews.item_id
    GROUP BY items.id 
    ORDER BY items.id DESC"""
    return db.query(sql)

def get_item(item_id):
    sql= """SELECT items.id, items.title, items.description, items.story, users.id user_id, users.username FROM items, users WHERE items.user_id = users.id AND items.id=?"""
    result= db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, description, story, classes):
    sql= """UPDATE items SET title = ?, description = ?, story = ? WHERE id = ?"""
    db.execute(sql, [title, description, story, item_id])

    sql="DELETE FROM item_classes WHERE item_id=?"
    db.execute(sql, [item_id])

    sql="INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def remove_item(item_id):
    sql= "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql= "DELETE FROM reviews WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql= "DELETE FROM images WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql= "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql= """SELECT id, title FROM items WHERE title LIKE ? OR description LIKE ? ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def get_images(item_id):
    sql="SELECT id FROM images WHERE item_id=?"
    result=db.query(sql, [item_id])
    return result 

def add_image(item_id, image):
    sql="INSERT INTO images (item_id, image) VALUES (?, ?)"
    
    db.execute(sql, [item_id, image])

def get_image(image_id):
    sql="SELECT id, image FROM images WHERE id=?"
    result=db.query(sql, [image_id])

    return result[0][0] if result else None
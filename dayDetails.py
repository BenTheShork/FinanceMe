from database import get_db, close_db


def getItemsByDay(user_id, day):
    """
    Returnes item depending on a day and user
    """

    db = get_db()
    query = """
    SELECT summary.id, item.item, item.price, category.category
    FROM item 
    INNER JOIN summary
    ON item.id = summary.item_id
    INNER JOIN category
    ON summary.category_id = category.id 
    INNER JOIN user 
    ON summary.user_id = user.id 
    WHERE summary.date = ? 
    AND user.id = ?
    """
    response = db.execute(query, (str(day), str(user_id), )).fetchall()
    return response


def populateCategories(user_id):
    """
    Populates categories from database by user id
    """

    db = get_db()
    query = """
    SELECT category.category
    FROM category
    INNER JOIN user
    ON user.id = category.user_id
    WHERE user.id  = ?
    """
    categories = db.execute(query, (str(user_id),)).fetchall()
    select = []
    for category in categories:
        select.append(category["category"])
    return select


def checkIfItemExists(item, price, description, user_id):
    """
    Cheks if item exists before adding to reduce redudance. DEPRECATED
    """

    db = get_db()
    query = """
    SELECT item.item 
    FROM item
    INNER JOIN summary
    ON item.id = summary.item_id
    INNER JOIN user
    ON user.id = summary.user_id
    WHERE item.item = ?
    AND item.price = ?
    AND item.description = ?
    AND user.id = ?
    """
    response = db.execute(query, (str(item), str(
        price), str(description), str(user_id), )).fetchall()
    if response:
        return True
    else:
        return False


def addItem(item, price, description, user_id, date, category):
    """
    Adds an item into the item table
    """

    # if not checkIfItemExists(item, price, description, user_id):
    db = get_db()
    query = """
    INSERT INTO item (item, price, description) VALUES (?, ?, ?);
    """
    db.execute(query, (str(item), str(price), str(description)))
    db.commit()
    addToSummary(user_id, category, date)


def addToSummary(user_id, category, date):
    """
    Checks if it is possible to add to summary and if it is, adds it
    """

    db = get_db()
    query = """
    SELECT id FROM item ORDER BY id DESC LIMIT 1;   
    """
    item_id = db.execute(query).fetchone()["id"]

    query = """
    SELECT id FROM category WHERE category = ? AND user_id = ?
    """

    response = db.execute(query, (str(category), str(user_id))).fetchone()
    category_id = response["id"]

    query = """
    INSERT INTO summary (user_id, item_id, category_id, date) VALUES (?, ?, ?, ?);
    """
    db.execute(query, (str(user_id), str(item_id),
               str(category_id), str(date),))
    db.commit()


def deleteItemFromDB(id):
    """ 
    Deletes item by its id
    """

    db = get_db()
    query = """
    DELETE FROM summary 
    WHERE id = ?
    """
    db.execute(query, (str(id), ))
    db.commit()

from database.database import get_db, close_db

def getCategories(user_id):
    """
    Returns categories based on user id
    """
    db = get_db()
    query = """
        SELECT category.category
        FROM category 
        INNER JOIN summary 
        ON category.id = summary.category_id
        INNER JOIN user
        ON summary.user_id = user.id WHERE user.id = ?
        """
    response = db.execute(query, str(user_id)).fetchall()
    return response


def groupByCategories(user_id):
    """
    Returns number of occurences of categories (GROUP BY)
    """
    db = get_db()
    query = """
        SELECT category.id, category.category, COUNT(summary.id) AS occurence, SUM(item.price) AS total
        FROM category
        LEFT JOIN summary ON category.id = summary.category_id
        LEFT JOIN item ON summary.item_id = item.id
        WHERE category.user_id = ? 
        GROUP BY category.id;
        """

    response = db.execute(query, (str(user_id), )).fetchall()
    return response


def setCategoryById(category_id, category):
    """
    Renames category by its id
    """
    db = get_db()
    query = """
        UPDATE category
        SET category = ?
        WHERE id = ?;
        """
    db.execute(query, (str(category), str(category_id)))
    db.commit()


def getCategoryById(category_id, user_id):
    """
    Breaks down all inflows/outflows from category with this id
    """
    db = get_db()
    query = """
        SELECT c.id, s.date, c.category, i.item, i.price
        FROM category c
        INNER JOIN summary s ON c.id = s.category_id
        INNER JOIN item i ON s.item_id = i.id
        WHERE s.user_id = ?
        AND s.category_id = ? 
        """

    response = db.execute(query, (str(user_id), str(category_id), )).fetchall()

    if not response:
        query = """
                SELECT category.id, category.category
                FROM category
                INNER JOIN user
                ON category.user_id = user.id
                WHERE user.id = ?
                AND category.id = ? 
                """
        response = db.execute(
            query, (str(user_id), str(category_id), )).fetchall()
    return response


def addCategory(category, user_id):
    """
    Adds a new category to the database for a specific user
    """
    if not checkIfCategoryExists(category, user_id):
        db = get_db()
        query = """
                INSERT INTO category (category, user_id) VALUES (?, ?)
                """
        db.execute(query, (str(category), str(user_id), ))
        db.commit()


def checkIfCategoryExists(category, user_id):
    db = get_db()
    query = """
        SELECT category FROM category WHERE category = ? AND user_id = ?
        """
    response = db.execute(query, (str(category), str(user_id),)).fetchone()
    if response:
        return True
    else:
        return False


def deleteCategoryFromDb(user_id, category_id):
    """
    Deletes category based on its and users id
    """
    db = get_db()
    query = """
        DELETE FROM category 
        WHERE user_id = ?
        AND id = ?
        
        """
    db.execute(query, (str(user_id), str(category_id), ))
    db.commit()

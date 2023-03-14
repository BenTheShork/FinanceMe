from database import get_db, close_db
import calendar

def checkIfUserExists(username):
        """
        Function searches for username in the database.
        If user is found returns true, otherwise - false.
        """
        db = get_db()
        query = """
        SELECT username 
        FROM user 
        WHERE username = ?
        """ 
        response = db.execute(query, (str(username),)).fetchone()
        if response:
                return True
        else:
                return False

def registerUser(username, password, name, surname):
        """
        Using the credentials provided on the register page, adds user to the 'user' table.
        """
        createNewSetting()
        lastSettingId = getLastSetting()
        db = get_db()
        query = """
        INSERT INTO user
        (username, password, name, surname, settings_id)
        VALUES (?, ?, ?, ?, ?)
        """ 
        db.execute(query, (str(username), str(password), str(name), str(surname), str(lastSettingId)))
        db.commit()
        

def createNewSetting():
        """
        Create new setting in settings table corresponding to user
        """
        
        db = get_db()
        query = """
        INSERT INTO settings
        (daily_limit, monthly_limit)
        VALUES (?, ?)
        """ 
        db.execute(query, (str(100), str(5000), ))
        db.commit()

def getLastSetting():
        db = get_db()
        query = """
        SELECT id 
        FROM settings
        ORDER BY id DESC LIMIT 1
        """ 
        response = db.execute(query).fetchone()
        return response[0]
        

def checkLoginAndPassword(username):
        """
        Checks if credentials are correct.
        Returns raw query response.
        """
        db = get_db()
        query = """
        SELECT id, username, password
        FROM user 
        WHERE username = ?
        """
        response = db.execute(query, (str(username),)).fetchone()
        
        return response
       
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
        response = db.execute(query, (str(user_id), )).fetchall()
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
        db.execute(query, (str(category), str(category_id) ))
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
                response = db.execute(query, (str(user_id), str(category_id), )).fetchall()
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

def deleteCategory1(user_id, category_id):
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

def getSettingsById(user_id):
        """
        Returns settings for a specific user
        """
        db = get_db()
        query = """
        SELECT *
        FROM settings
        INNER JOIN user
        ON settings.id = user.settings_id
        WHERE user.id = ? 
        """
        response = db.execute(query, (str(user_id))).fetchone()
        return response

def setSettings(user_id, monthly_limit, daily_limit):
        """
        Updates settings by user_id, montly_limit and daily_id
        """
        db = get_db()
        query = """
        UPDATE settings
        SET daily_limit = ?, monthly_limit = ?
        WHERE id = ?
        """
        db.execute(query, (str(daily_limit), str(monthly_limit), str(user_id),  ))
        db.commit()
        
def createCalendar(year, user_id):
    """
    Creates calendar for this year on a home page depending on user
    """
    months = []
    data = getTotalByDay(user_id)
    for month in range(1, 13):
        days_in_month = calendar.monthrange(year, month)[1]
        first_day_of_month = calendar.weekday(year, month, 1)
        weeks = ((days_in_month + first_day_of_month) // 7) + 1
        month_dict = {
            "month": month,
            "year": year,
            "days": [],
            "total": 0,
        }
        for row in range(weeks):
            week = []
            for col in range(7):
                current_day = ((row * 7) + col + 1) - first_day_of_month
                if current_day >= 1 and current_day <= days_in_month:
                    date = str(current_day) + "." + str(month) + "." + str(year)
                    total = 0
                    for item in data:
                        if item["date"] == date:
                                total = item["total"]
                                break
                    month_dict["total"] += total
                    week.append({
                        "day": current_day,
                        "total": total,
                        "fullDate": date
                    })
                else:
                    week.append(None)
            month_dict["days"].append(week)
        months.append(month_dict)
    return months


def getTotalByDay(user_id):
    """
    Returns total expense/income of a user with that id
    """
    db = get_db()
    query = """
    SELECT date, SUM(price) as total
    FROM summary
    JOIN item ON summary.item_id = item.id
    WHERE summary.user_id = ?
    GROUP BY date;
    """
    response = db.execute(query, (str(user_id),)).fetchall()
    return [{"date": row[0], "total": row[1]} for row in response]


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
    categories = db.execute(query, str(user_id), ).fetchall()
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
    response = db.execute(query, (str(item), str(price), str(description), str(user_id), )).fetchall()
    if response:
        return True
    else:
        return False
    
    
    
def addItem(item, price, description, user_id, date, category):
    """
    Adds an item into the item table
    """
    
    #if not checkIfItemExists(item, price, description, user_id):
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
    
    response = db.execute(query, (str(category),str(user_id))).fetchone()
    category_id = response["id"]
    
    
    query = """
    INSERT INTO summary (user_id, item_id, category_id, date) VALUES (?, ?, ?, ?);
    """
    db.execute(query, (str(user_id), str(item_id), str(category_id), str(date),))
    db.commit()

def deleteItem1(id):
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
    

def format_date(date_str):
    """
    Formats dates in a same way the database does    
    """
    components = date_str.split("-")
    year = components[0]
    month = int(components[1])
    day = int(components[2])
    return f"{day}.{month}.{year}"


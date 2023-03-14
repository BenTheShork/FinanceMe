from database.database import get_db, close_db

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
    db.execute(query, (str(username), str(password),
               str(name), str(surname), str(lastSettingId)))
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

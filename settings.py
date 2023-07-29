from database import get_db, close_db


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
    response = db.execute(query, (str(user_id),)).fetchone()
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
    db.execute(query, (str(daily_limit), str(monthly_limit), str(user_id),))
    db.commit()

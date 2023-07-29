from database import get_db, close_db
import calendar


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
                    date = str(current_day) + "." + \
                        str(month) + "." + str(year)
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


def format_date(date_str):
    """
    Formats dates in a same way the database does    
    """
    components = date_str.split("-")
    year = components[0]
    month = int(components[1])
    day = int(components[2])
    return f"{day}.{month}.{year}"

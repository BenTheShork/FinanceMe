from flask import Flask, render_template, request, session, redirect, url_for, g
from flask_session import Session
from forms.forms import loginForm, categoryForm, registerForm, settingsForm, itemForm
from functionalities.authorisation import *
from functionalities.categories import *
from functionalities.dayDetails import *
from functionalities.settings import *
from functionalities.summary import *
from flask import Flask, redirect
from functools import wraps
from datetime import datetime
import werkzeug

app = Flask(__name__)
app.config["SECRET_KEY"] = "keyIsverySecret"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.context_processor
def inject_active():
    def is_active(endpoint):
        return 'active' if request.endpoint == endpoint else ''
    return dict(is_active=is_active)


@app.before_request
def logged_in_user():
    g.user = session.get("user_id", None)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if not is_authenticated():
        session.clear()
    message = ""
    form = loginForm()
    print(request.method)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        data = checkLoginAndPassword(username)
        if data:
            if werkzeug.security.check_password_hash(data["password"], password):
                session["user_id"] = data["id"]
                return redirect(url_for('calendar'))
            else:
                message = "Your credentials were incorrect"
        else:
            message = "Your credentials were incorrect"
    else:
        return render_template("login.html", form=form, message=message)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = registerForm()
    message = ""
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        surname = form.surname.data

        if checkIfUserExists(username):
            message = "A user with this username already exists. Try being more original ¯\_(ツ)_/¯"
        else:
            passwordHashed = werkzeug.security.generate_password_hash(password)
            registerUser(username, passwordHashed, name, surname)
            return redirect(url_for('login'))
    return render_template("register.html", form=form, message=message)


@app.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    message = ""
    user_id = session["user_id"]
    categories = groupByCategories(user_id)
    form = categoryForm()
    if form.validate_on_submit():
        category = form.category.data
        addCategory(category, user_id)
        return redirect(url_for("categories"))
    return render_template("categories.html", categories=categories, form=form)


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    form = categoryForm()
    user_id = session["user_id"]
    if form.validate_on_submit():
        category = form.category.data
        setCategoryById(category_id, category)
        return redirect(url_for("categories"))
    items = getCategoryById(category_id, user_id)
    if items:
        form.category.data = items[0]["category"]
    return render_template("edit_category.html", form=form, items=items)


@app.route("/delete_category/<int:category_id>", methods=["GET", "POST"])
def deleteCategory(category_id):

    user_id = session["user_id"]
    deleteCategoryFromDb(user_id, category_id)
    return redirect(url_for('categories'))


@app.route("/add_category", methods=["GET", "POST"])
@login_required
def add_category():
    form = categoryForm()
    user_id = session["user_id"]
    if form.validate_on_submit():
        category = form.category.data
        addCategory(category, user_id)
        return redirect(url_for("categories"))
    return render_template("add_category.html", form=form)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = settingsForm()
    user_id = session["user_id"]
    settings = getSettingsById(user_id)
    message = ""
    if form.validate_on_submit():
        daily_limit = form.daily_limit.data
        monthly_limit = form.monthly_limit.data
        if daily_limit < monthly_limit:
            setSettings(settings["id"], monthly_limit, daily_limit)
        else:
            message = "Daily limit can not be higher than monthly limit!"
    form.daily_limit.data = float(settings["daily_limit"])
    form.monthly_limit.data = float(settings["monthly_limit"])
    return render_template("settings.html", form=form, message=message)


@app.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():
    user_id = session["user_id"]
    months = createCalendar(2023, user_id)
    settings = getSettingsById(user_id)
    daily_limit = float(settings["daily_limit"])
    now = datetime.today().strftime('%Y-%m-%d')
    date = format_date(now)
    return render_template('calendar.html', months=months, daily_limit=daily_limit, date=date)


@app.route("/day_details/<string:day>", methods=["GET", "POST"])
@login_required
def day_details(day):
    user_id = session["user_id"]
    items = getItemsByDay(user_id, day)
    categories = populateCategories(user_id)
    form = itemForm()
    form.category.choices = categories

    if form.validate_on_submit():
        selectedCategory = form.category.data
        item = form.item.data
        price = form.price.data
        description = form.description.data
        date = day

        addItem(item, price, description, user_id, date, selectedCategory)
        return redirect(url_for('day_details', day=day))

    return render_template('day_details.html', items=items, day=day, form=form)


@app.route("/delete_item/<string:day>/<int:summary_id>", methods=["GET", "POST"])
def deleteItem(day, summary_id):
    deleteItemFromDB(summary_id)
    return redirect(url_for('day_details', day=day))


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.context_processor
def is_authenticated():
    def check_authenticated():
        if "user_id" in session:
            return True
        else:
            return False
    return {'is_authenticated': check_authenticated}

import os
import pytz
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    current_stocks = db.execute("SELECT symbol, SUM(noshares) AS noshares FROM transactions where id = :user_id and transaction_type <> :add_funds GROUP BY symbol HAVING noshares <> 0", user_id=session["user_id"],add_funds="ADD FUNDS")

    cash = db.execute("SELECT cash FROM users WHERE id = :user_id",user_id=session["user_id"])
    cash = cash[0]["cash"]
    cash_available = cash

    cashinvested = db.execute("SELECT cashinvested FROM users WHERE id = :user_id",user_id=session["user_id"])
    cash_invested = cashinvested[0]["cashinvested"]

    quote = {}

    for stock in current_stocks:
        quote[stock["symbol"]] = lookup(stock["symbol"])
        cash += quote[stock["symbol"]]["price"]*stock["noshares"]
    overall_balance = cash-cash_invested
    return render_template("index.html",current_stocks=current_stocks,quote=quote,cash=cash,overall_balance=overall_balance, cash_available=cash_available)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            flash("Invalid symbol")
            return render_template("buy.html")

        no_of_shares = request.form.get("shares")
        try:
            noshares = int(no_of_shares)
            if noshares <= 0:
                flash("Number of shares only accept a positive integer!")
                return render_template("buy.html")

        except ValueError:
            flash("Number of shares only accept a positive integer!")
            return render_template("buy.html")

        total_purchase = noshares*(quote["price"])
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash = rows[0]["cash"]

        if total_purchase > cash:
            flash("Not enough cash!")
            return render_template("buy.html")

        else:
            cash = cash - total_purchase
            db.execute("UPDATE users SET cash=:cash WHERE id = :user_id", cash=cash,user_id=session["user_id"])
            aux = 0

            db.execute("INSERT INTO transactions (transaction_type, symbol, price, time, noshares, id) VALUES(:transaction_type, :symbol, :price, :time, :noshares, :user_id)", user_id=session["user_id"],symbol=quote["symbol"],noshares=noshares,price=quote["price"],transaction_type="BUY",time=datetime.datetime.now(pytz.timezone('Brazil/East')))


            flash(f"Bought {noshares} {quote['symbol']} share(s) for USD {quote['price']} each!")
            return render_template("buy.html")

    return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    transactions_info = db.execute("SELECT * FROM transactions WHERE id = :user_id", user_id=session['user_id'])

    quote = {}

    for stock in transactions_info:
        if stock["symbol"] != "----":
            quote[stock["symbol"]] = lookup(stock["symbol"])


    return render_template("history.html", transactions_info=transactions_info,quote=quote)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if request.form['submit_button'] == 'login':
            # Ensure username was submitted
            if not request.form.get("username"):
                flash("Must provide username!")
                return render_template("login.html")

            # Ensure password was submitted
            elif not request.form.get("password"):
                flash("Must provide password!")
                return render_template("login.html")

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
                flash("Invalid username and/or password!")
                return render_template("login.html")

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")

        else:
           return render_template("passchange.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            flash("Invalid symbol")
            return render_template("quote.html")
        else:
            return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")

@app.route("/passchangeloggedin", methods=["GET", "POST"])
@login_required
def passchangeloggedin():
    if request.method == "POST":

        user_info = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])

        if not request.form.get("password"):
            flash("Must provide your current password!")
            return render_template("passchange.html")

        elif not request.form.get("newpassword"):
            flash("Must provide a new password!")
            return render_template("passchange.html")

        elif not request.form.get("newconfirmation"):
            flash("Must provide password confirmation!")
            return render_template("passchange.html")

        elif not request.form.get("newpassword") == request.form.get("newconfirmation"):
            flash("Passwords don't match!")
            return render_template("passchange.html")

        elif not check_password_hash(user_info[0]["hash"], request.form.get("password")):
            flash("Invalid current password")
            return render_template("passchange.html")

        elif check_password_hash(user_info[0]["hash"], request.form.get("newpassword")):
            flash("Must provide a new password!")
            return render_template("passchange.html")

        else:
            hash = generate_password_hash(request.form.get("newpassword"))
            db.execute("UPDATE users SET hash = :hash WHERE username = :username", hash=hash, username=user_info[0]['username'])
            flash("Password updated!")
            return redirect("/")
    else:
        return render_template("passchange.html")

@app.route("/passchangenotloggedin", methods=["GET", "POST"])
def passchangenotloggedin():
    if request.method == "POST":
        if not request.form.get("username"):
            flash("Must provide username!")
            return render_template("passchange.html")

        user_info = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        if not user_info:
            flash("Invalid username")
            return render_template("passchange.html")

        elif not request.form.get("password"):
            flash("Must provide your current password!")
            return render_template("passchange.html")

        elif not request.form.get("newpassword"):
            flash("Must provide a new password!")
            return render_template("passchange.html")

        elif not request.form.get("newconfirmation"):
            flash("Must provide password confirmation!")
            return render_template("passchange.html")

        elif not request.form.get("newpassword") == request.form.get("newconfirmation"):
            flash("Passwords don't match!")
            return render_template("passchange.html")

        elif not check_password_hash(user_info[0]["hash"], request.form.get("password")):
            flash("Invalid current password")
            return render_template("passchange.html")

        elif check_password_hash(user_info[0]["hash"], request.form.get("newpassword")):
            flash("Must provide a new password!")
            return render_template("passchange.html")

        else:
            hash = generate_password_hash(request.form.get("newpassword"))
            db.execute("UPDATE users SET hash = :hash WHERE username = :username", hash=hash, username=user_info[0]['username'])
            flash("Password updated!")
            return render_template("login.html")
    else:
        return render_template("passchange.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            flash("Must provide username!")
            return render_template("register.html")

        elif not request.form.get("password"):
            flash("Must provide password!")
            return render_template("register.html")

        elif not request.form.get("confirmation"):
            flash("Must provide password confirmation!")
            return render_template("register.html")

        elif not request.form.get("password") == request.form.get("confirmation"):
            flash("Passwords don't match!")
            return render_template("register.html")

        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO users (username,hash) VALUES(:username,:hash)", username=request.form.get("username"), hash=hash)
        if not new_user_id:
            flash("Username already in use")
            return render_template("register.html")

        flash("Registered!")

        session["user_id"] = new_user_id
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/addfunds", methods=["GET","POST"])
@login_required
def addfunds():
    if request.method == "POST":
        funds = request.form.get("funds")
        try:
            funds = float(funds)
            if funds <= 0:
                flash("You can only ADD to your funds!")
                return render_template("sell.html")

        except ValueError:
            flash("You can only add numbers!")
            return redirect("/")

        funds = float(funds)

        cash = db.execute("SELECT cash, cashinvested FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash_invested = float(cash[0]['cashinvested']) + funds
        newcash = float(cash[0]['cash']) + funds

        db.execute("UPDATE users SET cash=:cash, cashinvested=:cash_invested WHERE id=:user_id", user_id=session['user_id'], cash=newcash,cash_invested=cash_invested)
        db.execute("INSERT INTO transactions (transaction_type, symbol, price, time, noshares, id) VALUES (:transaction_type,:symbol,:price,:time,:noshares,:id)", symbol="----", transaction_type="ADD FUNDS",price=funds,time=datetime.datetime.now(pytz.timezone('Brazil/East')),noshares=1,id=session["user_id"])
        flash(f"Added {funds} to your funds.")
        return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == ("GET"):
        return render_template("sell.html")
    else:
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            flash("Invalid symbol")
            return render_template("sell.html")

        no_of_shares = request.form.get("shares")
        try:
            noshares = int(no_of_shares)
            if noshares <= 0:
                flash("Number of shares only accept a positive integer!")
                return render_template("sell.html")

        except ValueError:
            flash("Number of shares only accept a positive integer!")
            return render_template("sell.html")

        current_stocks = db.execute("SELECT SUM(noshares) AS noshares FROM transactions WHERE id = :user_id and symbol = :symbol GROUP BY symbol HAVING noshares!=0", symbol=quote["symbol"],user_id=session["user_id"])
        if (not current_stocks):
            flash(f"You don't have enough shares to sell. Current: 0x {quote['symbol']}")
            return render_template("sell.html")

        elif noshares > current_stocks[0]['noshares']:
            current = current_stocks[0]['noshares']
            flash(f"You don't have enough shares to sell. Current: {current}x {quote['symbol']}")
            return render_template("sell.html")
        else:
            db.execute("INSERT INTO transactions (transaction_type, symbol, price, time, noshares, id) VALUES (:transaction_type, :symbol, :price, :time, :noshares, :id)",transaction_type='SELL',symbol=quote["symbol"],price=quote["price"], time=datetime.datetime.now(pytz.timezone('Brazil/East')),noshares=-noshares,id=session["user_id"])
            current_cash = db.execute("SELECT cash FROM users WHERE id = :user_id",user_id = session["user_id"])
            current_cash = current_cash[0]['cash']
            current_cash = current_cash + noshares*quote['price']
            db.execute("UPDATE users SET cash = :newcash WHERE id = :user_id", newcash=current_cash, user_id=session['user_id'])
            flash(f"Sold {noshares} {quote['symbol']} share(s) for USD {quote['price']} each!")
            return render_template("sell.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

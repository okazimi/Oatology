# # IMPORTS
# FLASK SERVER IMPORT
from flask import Flask, render_template, request, redirect, url_for, flash
# FLASK BOOTSTRAP IMPORT
from flask_bootstrap import Bootstrap
# FLASK LOGIN IMPORT
from flask_login import login_user, LoginManager, current_user, logout_user
# DATABASE MODELS IMPORT
from models import db, User, Product
# PASSWORD SECURITY IMPORT
from werkzeug.security import generate_password_hash, check_password_hash
# OS IMPORT
import os


# FLASK/BOOTSTRAP CONFIGURATIONS
# CREATE FLASK APPLICATION
app = Flask(__name__)
# ASSIGN APPLICATIONS SECRET KEY
# ENSURE CONTENT IS MODIFIED ONLY BY THOSE AUTHORIZED (USED TO SIGN SESSION COOKIES)
app.secret_key = os.environ['SECRETKEY']
# INITIALIZE BOOTSTRAP EXTENSION
Bootstrap(app)


# LOGIN MANAGER CONFIGURATIONS
# CREATE LOGIN MANAGER OBJECT
login_manager = LoginManager()
# ALLOCATE LOGIN MANAGER TO APP
login_manager.init_app(app)


# DATABASE CONFIGURATIONS
# SPECIFY DB PATH
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
# SET TRACK MODIFICATIONS TO FALSE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# INITIALIZE DATABASE FOR APP
db.init_app(app)
# # CREATE DATABASE TABLES
# with app.app_context():
#     db.create_all()


# CREATE USER LOADER CALLBACK FOR LOGIN MANAGER
# THIS CALLBACK IS USED TO RELOAD THE USER OBJECT FROM THE USER_ID STORED IN THE SESSION
@login_manager.user_loader
def load_user(user_id):
    # RETURN A USER FROM THE USER TABLE IN THE OATOLOGY DATABASE BASED ON THE USER_ID
    return User.query.get(int(user_id))


# HOME PAGE (ACCEPTED METHODS = "GET")
@app.route("/", methods=["GET"])
def home():
    # QUERY PRODUCT TABLE
    product = db.get_or_404(Product, 1)
    # RENDER HOME PAGE
    return render_template("index.html", current_user=current_user, product=product)


# REGISTER PAGE (ACCEPTED METHODS: GET, POST)
@app.route("/register", methods=["GET", "POST"])
def register():
    # IF USER ATTEMPTS TO REGISTER
    if request.method == "POST":
        # CREATE USER OBJECT
        user = User(
            # GET USERS ENTERED EMAIL
            email=request.form.get("email"),
            # GET AND HASH USERS ENTERED PASSWORD
            password=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        )
        # IF USER DOES NOT EXIST
        if not User.query.filter_by(email=user.email).first():
            # ADD USER TO DATABASE
            db.session.add(user)
            db.session.commit()
            # LOGIN USER
            login_user(user)
            # REDIRECT USER TO HOME PAGE
            return redirect(url_for('home'))
        # IF USER DOES EXIST
        else:
            # GENERATE FLASH MESSAGE
            flash("The provided email already exists, please login instead")
            # REDIRECT USER TO LOGIN PAGE
            return redirect(url_for('login'))
    # RENDER REGISTER PAGE
    return render_template("register.html", current_user=current_user)


# LOGIN PAGE (ACCEPTED METHODS: GET, POST)
@app.route("/login", methods=["GET", "POST"])
def login():
    # IF USER ATTEMPTS TO LOGIN
    if request.method == "POST":
        # GET USERS ENTERED EMAIL
        email = request.form.get("email")
        # GET USERS ENTERED PASSWORD
        password = request.form.get("password")
        # CHECK IF USER IS IN DATABASE
        user = User.query.filter_by(email=email).first()
        # IF USER DOES NOT EXIST
        if not user:
            # GENERATE FLASH MESSAGE
            flash("The email entered does not exist. Please try again or register instead")
        # IF USER DOES EXIST
        else:
            # IF USER ENTERED CORRECT PASSWORD
            if check_password_hash(user.password, password):
                # LOGIN USER
                login_user(user)
                # REDIRECT USER TO HOME PAGE
                return redirect(url_for('home'))
            # IF USER ENTERED INCORRECT PASSWORD
            else:
                # GENERATE FLASH MESSAGE
                flash("The password entered is incorrect. Please try again")
    # RENDER LOGIN PAGE
    return render_template("login.html", current_user=current_user)


# LOGOUT
@app.route('/logout')
def logout():
    # LOGOUT CURRENT USER
    logout_user()
    # REDIRECT USER TO HOME PAGE
    return redirect(url_for('home'))


# CART PAGE (ACCEPTED METHODS: GET, POST)
@app.route('/cart/', methods=["GET", "POST"])
@app.route('/cart/<int:product_id>', methods=["GET", "POST"])
def cart(product_id=None):
    # IF USER ADDS ITEM TO CART
    if request.method == "POST":
        # GET PRODUCT FROM DATABASE
        product = Product.query.get(product_id)
        print(product.id)
        print(product.name)
        print(product.price)
        print(product.image)
    # RENDER CART PAGE
    return render_template("cart.html", current_user=current_user, product_id=product_id)


if __name__ == "__main__":
    # RUN FLASK APPLICATION IN DEBUG MODE
    app.run(debug=True)

import os
from dotenv import load_dotenv

from flask import Flask

from backend.db_connection import db

from backend.customers.customer_routes import customers
from backend.products.products_routes import products
from backend.simple.simple_routes import simple_routes

from backend.users.users_routes import users
from backend.departments.departments_routes import departments
from backend.posts.post_routes import posts
from backend.comments.comments_routes import comments
from backend.tags.tag_routes import tags


def create_app():
    app = Flask(__name__)

    # Load env vars from our .env file 
    load_dotenv()

    # Secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()  # Change this to your DB name

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)


    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(simple_routes)
    app.register_blueprint(customers,   url_prefix='/c')
    app.register_blueprint(products,    url_prefix='/p')

    app.register_blueprint(posts,       url_prefix='/po')
    app.register_blueprint(comments,    url_prefix='/cmt')
    app.register_blueprint(departments, url_prefix='/dept')
    app.register_blueprint(tags, url_prefix='/t')
    app.register_blueprint(users,       url_prefix='/u')
    app.register_blueprint(tags, url_prefix='/t')

    # Don't forget to return the app object
    return app


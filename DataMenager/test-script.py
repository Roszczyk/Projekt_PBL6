from flask import Flask, jsonify, request
import mysql.connector
import hashlib
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_pymongo import PyMongo
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://10.141.10.69:27017/data_db'
mongo = PyMongo(app)

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'User and Hive Management API'}
)

# Database configuration
db_config = {
    'host': '10.141.10.69',
    'port': '3333',
    'user': 'root',
    'password': 'password',
    'database': 'mysql'
}


def get_password_hash(password):
    """Generate password hash using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(username, password):
    """Add a new user with password hash to the database."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(query, (username, get_password_hash(password)))
    connection.commit()
    cursor.close()
    connection.close()


def remove_user(username):
    """Remove a user from the database."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "DELETE FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    connection.commit()
    cursor.close()
    connection.close()


def get_all_users():
    """Get all users from the database."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT username FROM users"
    cursor.execute(query)
    users = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return users


def add_hive_to_user(user_id, hive_id):
    """Add a hive to a certain user."""
    mongo.db.hives.update_one(
        {'user_id': user_id},
        {'$addToSet': {'hives': hive_id}},
        upsert=True
    )


def remove_hive_from_user(user_id, hive_id):
    """Remove a hive from a certain user."""
    mongo.db.hives.update_one(
        {'user_id': user_id},
        {'$pull': {'hives': hive_id}}
    )


def get_user_hives(user_id):
    """Get all hives of a certain user."""
    user_hives = mongo.db.hives.find_one({'user_id': user_id})
    return user_hives.get('hives', []) if user_hives else []


if __name__ == '__main__':

    add_user('abba', '1234')
    add_hive_to_user('abba', 'hive1')
    print(get_user_hives('abba'))
    remove_hive_from_user('abba', 'hive1')
    remove_user('abba')

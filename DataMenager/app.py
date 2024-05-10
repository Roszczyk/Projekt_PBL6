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


@app.route('/add_user', methods=['POST'])
def add_user_route():
    """
    Add a new user with password.
    ---
    parameters:
      - name: username
        in: query
        description: The username to add.
        required: true
        type: string
      - name: password
        in: query
        description: The password for the user.
        required: true
        type: string
    responses:
        200:
            description: User added successfully.
            schema:
                type: object
                properties:
                    message:
                        type: string
        400:
            description: Invalid request or missing parameters.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: The error message.
    """
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    add_user(username, password)
    return jsonify({'message': 'User added successfully.'})


@app.route('/remove_user', methods=['DELETE'])
def remove_user_route():
    """
    Remove a user.
    ---
    parameters:
      - name: username
        in: query
        description: The username to remove.
        required: true
        type: string
    responses:
        200:
            description: User removed successfully.
            schema:
                type: object
                properties:
                    message:
                        type: string
        400:
            description: Invalid request or missing parameters.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: The error message.
    """
    username = request.args.get('username')
    if not username:
        return jsonify({'message': 'Username is required.'}), 400

    remove_user(username)
    return jsonify({'message': 'User removed successfully.'})


@app.route('/add_hive_to_user', methods=['POST'])
def add_hive_to_user_route():
    """
    Add a hive to a certain user.
    ---
    parameters:
      - name: user_id
        in: query
        description: The ID of the user to add the hive to.
        required: true
        type: string
      - name: hive_id
        in: query
        description: The ID of the hive to add.
        required: true
        type: string
    responses:
        200:
            description: Hive added to user successfully.
            schema:
                type: object
                properties:
                    message:
                        type: string
        400:
            description: Invalid request or missing parameters.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: The error message.
    """
    user_id = request.args.get('user_id')
    hive_id = request.args.get('hive_id')

    if not user_id or not hive_id:
        return jsonify({'message': 'User ID and hive ID are required.'}), 400

    add_hive_to_user(user_id, hive_id)
    return jsonify({'message': 'Hive added to user successfully.'})


@app.route('/remove_hive_from_user', methods=['DELETE'])
def remove_hive_from_user_route():
    """
    Remove a hive from a certain user.
    ---
    parameters:
      - name: user_id
        in: query
        description: The ID of the user to remove the hive from.
        required: true
        type: string
      - name: hive_id
        in: query
        description: The ID of the hive to remove.
        required: true
        type: string
    responses:
        200:
            description: Hive removed from user successfully.
            schema:
                type: object
                properties:
                    message:
                        type: string
        400:
            description: Invalid request or missing parameters.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: The error message.
    """
    user_id = request.args.get('user_id')
    hive_id = request.args.get('hive_id')

    if not user_id or not hive_id:
        return jsonify({'message': 'User ID and hive ID are required.'}), 400

    remove_hive_from_user(user_id, hive_id)
    return jsonify({'message': 'Hive removed from user successfully.'})


@app.route('/get_user_hives', methods=['GET'])
def get_user_hives_route():
    """
    Get all hives of a certain user.
    ---
    parameters:
      - name: user_id
        in: query
        description: The ID of the user to get hives for.
        required: true
        type: string
    responses:
        200:
            description: The list of hives.
            schema:
                type: object
                properties:
                    user_id:
                        type: string
                    hives:
                        type: array
                        items:
                            type: string
        400:
            description: Invalid request or missing parameters.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: The error message.
        404:
            description: No hives found for the user.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: The error message.
    """
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'message': 'User ID is required.'}), 400

    hives = get_user_hives(user_id)
    if hives:
        return jsonify({'user_id': user_id, 'hives': hives})
    else:
        return jsonify({'message': 'No hives found for the user.'}), 404


@app.route('/list_users', methods=['GET'])
def list_users_route():
    """
    Get the list of all users.
    ---
    responses:
        200:
            description: The list of users.
            schema:
                type: object
                properties:
                    users:
                        type: array
                        items:
                            type: string
        404:
            description: No users found.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: The error message.
    """
    users = get_all_users()

    if users:
        return jsonify({'users': users}), 200
    else:
        return jsonify({'message': 'No users found.'}), 404


@app.route(API_URL)
def swagger_json():
    return jsonify(swagger(app))


app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, port=5002)

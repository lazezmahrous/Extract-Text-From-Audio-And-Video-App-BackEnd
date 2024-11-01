import uuid
from flask import Blueprint, request, jsonify
import hashlib
import os
import json

auth = Blueprint('auth', __name__)

USER_DATA_FOLDER = 'users_data'
os.makedirs(USER_DATA_FOLDER, exist_ok=True)

class User:
    def __init__(self, full_name, email, password_hash,token):
        self.token = token
        self.full_name = full_name
        self.email = email
        self.password_hash = password_hash

    def to_dict(self):
        return {
            "full_name": self.full_name,
            "email": self.email,
            "password": self.password_hash,
            "token": self.token
        }

    @staticmethod
    def from_dict(data):
        return User(
            full_name=data.get("full_name"),
            email=data.get("email"),
            password_hash=data.get("password"),
            token=data.get("token"),
        )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user_data(user):
    user_file_path = os.path.join(USER_DATA_FOLDER, f"{user.email}.json")
    with open(user_file_path, 'w', encoding='utf-8') as user_file:
        json.dump(user.to_dict(), user_file, ensure_ascii=False, indent=4)
        
def load_user_data(email):
    user_file_path = os.path.join(USER_DATA_FOLDER, f"{email}.json")
    if os.path.exists(user_file_path) and os.path.getsize(user_file_path) > 0:
        with open(user_file_path, 'r', encoding='utf-8') as user_file:
            return User.from_dict(json.load(user_file))
    else:
        return None
    
@auth.route('/signup', methods=['POST'])
def sign_up():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    token = uuid.uuid4().hex
    
    if not email or not password:
        return jsonify({"message": "Email and password are required" , "code":400}), 400

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match" , "code":400}), 400

    if load_user_data(email):
        return jsonify({"message": "Email already exists", "code":400}), 400

    password_hash = hash_password(password)
    user = User(full_name, email, password_hash, token)
    save_user_data(user)

    return jsonify({"token":token,"full_name":full_name,"message": "User created successfully","code":201 , "email":email}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"message": "Email and password are required" , "code":400}), 400

    user = load_user_data(email)

    if not user:
        return jsonify({"message": "User not found" , "code":404}), 404

    if user.password_hash != hash_password(password):
        return jsonify({"message": "Email Or Password Wrong" , "code":401}), 401

    
    return jsonify({"message": "Login successful" , "code":200 , "token":user.token , "email":email , "full_name":user.full_name}), 200

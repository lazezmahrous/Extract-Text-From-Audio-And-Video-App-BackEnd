from flask import Flask
from auth.auth_routes import auth
from service.service_routes import service

app = Flask(__name__)

# SetUp Blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(service, url_prefix='/service')

# # Fix arabic language
# app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run(debug=True , host='192.168.1.9')
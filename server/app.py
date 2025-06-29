from flask import Flask
from flask_restful import Api
from server.resources import Signup, CheckSession, Login, Logout, RecipeIndex

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Set your secret key here

api = Api(app)

# Add resources only once here
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')

if __name__ == "__main__":
    app.run(debug=True)

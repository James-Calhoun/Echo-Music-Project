from flask_app import app

# Import Controllers Below
from flask_app.controllers import posts
from flask_app.controllers import users

if __name__=="__main__":
    app.run(debug=True, port=5001)
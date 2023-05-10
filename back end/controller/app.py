from flask import Flask, request, jsonify
from flask_cors import CORS

#set flask up
app = Flask(__name__)

#set up flask to bypass CORS at the front end:
cors = CORS(app)

#run the app
if __name__ == "__main__":
    app.run(debug=True)
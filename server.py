import os
from flask import Flask
from flask import request
from static.methods.pipeline import pipeline
from flask import jsonify
try:
  from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
  from SocketServer import TCPServer as Server
except ImportError:
  from http.server import SimpleHTTPRequestHandler as Handler
  from http.server import HTTPServer as Server


app = Flask(__name__)


@app.route('/')
def welcome():
    return app.send_static_file('index.html')


@app.route('/pipeline', methods=['GET', 'POST'])
def pipeline_endpoint():
    if request.method == 'POST':
        print '\nPOST REQUEST RECEIVED TO PIPELINE ENDPOINT'

        # 1. Receive the Post request
        data = request.json

        # 2. Parse the word passed
        text = data["text"]

        # 3. Stopped text
        stopped_text = pipeline(text)

        # 4. Return the hash_list to the backend
        return (text)

    else:
        print '\nGET REQUEST RECEIVED TO PIPELINE ENDPOINT'
        return "You sent a get request to the syllable count endpoint you idiots"


# Read port selected by the cloud for our application
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))

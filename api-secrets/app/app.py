from flask import Flask
import os
import base64

app = Flask(__name__)

# load flag & delete
flag = open("/app/flag.txt").read().strip()
b64_flag = base64.b64encode(flag.encode('utf-8'))
os.remove("/app/flag.txt")

@app.route("/", methods=['GET'])
def index():
    return "Hello World\n"

@app.route("/api", methods=['GET'])
def api():
    return b64_flag
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  

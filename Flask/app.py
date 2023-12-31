# Import flask module
from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return 'Hello to Flask!'
 
# main driver function
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',ssl_context=('cert.pem','key.pem'))

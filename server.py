from flask import Flask, Response, render_template, request
from flask_cors import CORS
from blueprints.db_bp import station_bp
app = Flask(__name__)

    
app.register_blueprint(station_bp, url_prefix='/api')
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}},
     supports_credentials=True)

@app.route('/', methods=['GET'])
def get_index():
    return render_template(
        "index.html"
    )
try:
    if __name__ == '__main__':
        app.run(debug=True)
except Exception as ex:
    print(ex)
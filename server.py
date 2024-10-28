from flask import Flask, Response, redirect, render_template, request, url_for
from flask_cors import CORS
from blueprints.db_bp import station_bp
from blueprints.logreg_bp import logreg_bp
from blueprints.requests_bp import reqs_bp
app = Flask(__name__)


app.register_blueprint(station_bp, url_prefix='/api')
app.register_blueprint(logreg_bp, url_prefix='/api')
app.register_blueprint(reqs_bp, url_prefix='/api')
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}},
     supports_credentials=True)


@app.route('/', methods=['GET'])
def get_index():
    if (request.cookies.get('role') is None):
        return redirect('/logreg')
    return render_template(
        "index.html"
    )


@app.route('/logreg', methods=['GET'])
def get_logreg():
    return render_template(
        "logreg.html"
    )


@app.route('/req1', methods=['GET'])
def get_req1():
    return render_template(
        "requests/req1.html"
    )


@app.route('/req2', methods=['GET'])
def get_req2():
    return render_template(
        "requests/req2.html"
    )


@app.route('/req3', methods=['GET'])
def get_req3():
    return render_template(
        "requests/req3.html"
    )


@app.route('/req4', methods=['GET'])
def get_req4():
    return render_template(
        "requests/req4.html"
    )


@app.route('/req5', methods=['GET'])
def get_req5():
    return render_template(
        "requests/req5.html"
    )


@app.route('/req6', methods=['GET'])
def get_req6():
    return render_template(
        "requests/req6.html"
    )


@app.route('/req7', methods=['GET'])
def get_req7():
    return render_template(
        "requests/req7.html"
    )


@app.route('/req8', methods=['GET'])
def get_req8():
    return render_template(
        "requests/req8.html"
    )


@app.route('/req9', methods=['GET'])
def get_req9():
    return render_template(
        "requests/req9.html"
    )


@app.route('/req10', methods=['GET'])
def get_req10():
    return render_template(
        "requests/req10.html"
    )


@app.route('/queries', methods=['GET'])
def get_queries():
    return render_template(
        "queries.html"
    )


if __name__ == '__main__':
    app.run(debug=True)

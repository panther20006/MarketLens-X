from flask import Flask, jsonify
from flask_cors import CORS

from routes.search import search_bp
from routes.products import products_bp
from routes.compare import compare_bp
from routes.insights import insights_bp


app = Flask(__name__)

CORS(app)


app.register_blueprint(search_bp)
app.register_blueprint(products_bp)
app.register_blueprint(compare_bp)
app.register_blueprint(insights_bp)


@app.route("/")
def home():

    return jsonify({

        "name":
            "MarketLens X",

        "version":
            "1.0",

        "status":
            "online"

    })


@app.route("/api/health")
def health():

    return jsonify({

        "success":
            True,

        "message":
            "MarketLens backend is running"

    })


if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )
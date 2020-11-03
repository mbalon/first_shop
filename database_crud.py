import pathlib
from typing import Optional

from flask import Flask
from flask_sqlalchemy import request
from flask.json import jsonify
from models import db, Producer, Product


# This is factory function
def create_app(database_uri: Optional[str] = None) -> Flask:
    app = Flask(__name__)

    if database_uri is None:
        db_file_path = pathlib.Path(__file__).parent / "shop_24_10_20.db"
        database_uri = f"sqlite:///{db_file_path}"

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

    db.init_app(app)

    @app.route("/add_producer", methods=["POST"])
    def add_producer():
        data = request.get_json()
        try:
            producer = Producer(name=data["name"])
            db.session.add(producer)
            db.session.commit()
            return jsonify(producer.to_dict())
        except KeyError:
            response = jsonify({"error": "Bad request", "missing field": "name"})
            response.status_code = 400
            return response

    @app.route("/add_product", methods=["POST"])
    def add_product():
        data = request.get_json()
        try:
            product = Product(name=data["name"])
            db.session.add(product)
            db.session.commit()
            return jsonify(product.to_dict())
        except KeyError:
            response = jsonify({"error": "Bad request", "missing field": "name"})
            response.status_code = 400
            return response

    return app


if __name__ == '__main__':
    create_app("sqlite:///shop_24_10_20.db").run()

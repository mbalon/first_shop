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

    print(database_uri)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

    db.init_app(app)

    @app.route("/get_producers", methods=["GET"])
    def get_producers():
        return jsonify([producer.to_dict() for producer in db.session.query(Producer)])

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

    @app.route("/get_producer/<int:producer_id>", methods=["GET"])
    def get_producer(producer_id):
        producer = db.session.query(Producer).filter_by(id=producer_id).first_or_404
        return jsonify(producer.to_dict())

    @app.route("/get_product/<int:product_id>", methods=["GET"])
    def get_product(product_id):
        product = db.session.query(Product).filter_by(id=product_id).first_or_404
        return jsonify(product.to_dict())

    return app


if __name__ == '__main__':
    create_app("sqlite:///shop_24_10_20.db").run()

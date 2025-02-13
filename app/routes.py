from flask import Blueprint, request, jsonify
from app import db, redis_client
from app.models import Product


bp = Blueprint('products', __name__)

@bp.route('/products', methods=['GET'])
def get_products():
    cached_products = redis_client.get('products')
    if cached_products: return jsonify(eval(cached_products))

    products = Product.query.all()
    products_list = [p.to_dict() for p in products]
    redis_client.setex('products', 60, str(products_list))
    return jsonify(products_list)


@bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(
        name=data['name'], 
        description=data.get('description'), 
        price=data['price']
    )

    db.session.add(product)
    db.session.commit()

    redis_client.delete('products')
    return jsonify(product.to_dict(), 201)

    

from flask import Blueprint, jsonify
from models.promo_model import (
    get_promos_by_budget,
    get_promos_by_category,
    get_all_promos
)

promo_routes = Blueprint('promo_routes', __name__)


@promo_routes.route('/promos')
def promos():
    results = get_all_promos()

    promo_list = []

    for promo in results:
        promo_list.append({
            'id': promo[0],
            'name': promo[1],
            'category': promo[2],
            'price': float(promo[3]),
            'description': promo[4]
        })

    return jsonify(promo_list)


@promo_routes.route('/promos/budget/<int:budget>')
def budget_promos(budget):

    results = get_promos_by_budget(budget)

    promo_list = []

    for promo in results:
        promo_list.append({
            'id': promo[0],
            'name': promo[1],
            'category': promo[2],
            'price': float(promo[3]),
            'description': promo[4]
        })

    return jsonify(promo_list)


@promo_routes.route('/promos/category/<string:category>')
def category_promos(category):

    results = get_promos_by_category(category)

    promo_list = []

    for promo in results:
        promo_list.append({
            'id': promo[0],
            'name': promo[1],
            'category': promo[2],
            'price': float(promo[3]),
            'description': promo[4]
        })

    return jsonify(promo_list)
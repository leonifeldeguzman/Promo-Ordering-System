from unicodedata import category

from flask import Blueprint, jsonify, request, redirect, render_template
from models.promo_model import (
    get_promos_by_budget,
    get_promos_by_category,
    get_all_promos,
    get_promos_by_category_and_budget,
    add_menu_item,
    update_price,
    update_status,
    delete_menu_item
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

@promo_routes.route('/promos/<string:category>/<int:budget>')
def category_budget_promos(category, budget):

    results = get_promos_by_category_and_budget(category, budget)

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

@promo_routes.route('/admin')
def admin_page():

    results = get_all_promos()

    return render_template(
        'admin.html',
        items=results
    )


# =========================
# ADD ITEM
# =========================

@promo_routes.route('/add-item', methods=['POST'])
def add_item():

    name = request.form['item_name']
    category = request.form.get('category')
    price = request.form['price']
    promo_details = request.form.get('promo_details')
    status = request.form['status']

    add_menu_item(
        name,
        price,
        category,
        promo_details,
        status
    )

    return redirect('/admin')


# =========================
# UPDATE PRICE
# =========================

@promo_routes.route('/update-price/<int:item_id>', methods=['POST'])
def change_price(item_id):

    new_price = request.form['price']

    update_price(item_id, new_price)

    return redirect('/admin')


# =========================
# UPDATE STATUS
# =========================

@promo_routes.route('/update-status/<int:item_id>', methods=['POST'])
def change_status(item_id):

    status = request.form['status']

    update_status(item_id, status)

    return redirect('/admin')

# =========================
# DELETE STATUS
# =========================
@promo_routes.route('/delete-item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    delete_menu_item(item_id)
    return redirect('/admin')
import os

from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, request, redirect, render_template, session
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
from models.promo_model import update_item_details

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
            'description': promo[4] if promo[4] else "Special promo offer!",
            'promo_details': promo[5],
            'status': promo[6],
            'image': promo[7]
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
            'description': promo[4] if promo[4] else "Special promo offer!",
            'promo_details': promo[5],
            'status': promo[6],
            'image': promo[7]
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
            'description': promo[4] if promo[4] else "Special promo offer!",
            'promo_details': promo[5],
            'status': promo[6],
            'image': promo[7]
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
            'description': promo[4] if promo[4] else "Special promo offer!",
            'promo_details': promo[5],
            'status': promo[6],
            'image': promo[7]
        })
    
    return jsonify(promo_list)

@promo_routes.route('/admin')
def admin_page():
    if not session.get('admin_logged_in'):
        return redirect('/admin-login')

    results = get_all_promos()

    username = session.get('admin_logged_in')  # 👈 ADD THIS

    return render_template(
        'admin.html',
        items=results,
        username=username   # 👈 ADD THIS
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

    # IMAGE
    image = request.files['image']
    
    if image and image.filename:
        filename = secure_filename(image.filename)
        
        upload_folder = os.path.join('static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        image.save(file_path)
        
        # CHANGE THIS LINE - remove 'static/' from the path
        # OLD: image_url = f"static/uploads/{filename}"  
        # NEW:
        image_url = f"uploads/{filename}"  # Just store the relative path
    else:
        image_url = None

    # SAVE DATABASE
    add_menu_item(
        name,
        price,
        category,
        promo_details,
        status,
        image_url
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

@promo_routes.route("/update-item/<int:item_id>", methods=["POST"])
def update_item(item_id):

    data = request.get_json()

    name = data.get("name")
    category = data.get("category")
    price = data.get("price")
    status = data.get("status")
    promo = data.get("promo")

    update_item_details(
        item_id,
        name,
        category,
        price,
        promo,
        status
    )

    return jsonify({"success": True})
# =========================
# ADMIN LOGIN PAGE
# =========================

@promo_routes.route('/admin-login')
def admin_login_page():

    return render_template('admin_login.html')


# =========================
# ADMIN LOGIN
# =========================

@promo_routes.route('/admin-login', methods=['POST'])
def admin_login():

    username = request.form['username']
    password = request.form['password']

    # SIMPLE HARDCODED LOGIN
    if username == "admin" and password == "admin123":

        session['admin_logged_in'] = username

        return redirect('/admin')

    return "Invalid username or password"


# =========================
# ADMIN LOGOUT
# =========================

@promo_routes.route('/logout')
def logout():

    session.pop('admin_logged_in', None)

    return redirect('/admin-login')


# =========================
# HOMEPAGE
# =========================

@promo_routes.route('/')
def homepage():

    return render_template('homepage.html')


# =========================
# VOICE ASSISTANT PAGE
# =========================

@promo_routes.route('/voice-assistant')
def voice_assistant():

    return render_template('index.html')


# =========================
# PROMOS PAGE
# =========================

@promo_routes.route('/promos-page')
def promos_page():

    results = get_all_promos()

    return render_template(
        'promos.html',
        promos=results
    )
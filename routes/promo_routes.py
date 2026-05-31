import os
import re
from models.promo_model import db_connection
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
    serving_size = request.form.get('serving_size')

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
        image_url,
        serving_size
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
    serving_size = data.get("serving_size")

    update_item_details(
        item_id,
        name,
        category,
        price,
        promo,
        status,
        serving_size
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

    if username == "admin" and password == "admin123":
        session['admin_logged_in'] = username
        return redirect('/admin')

    return render_template("admin_login.html", error="Invalid username or password")


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

    # get selected category from URL
    selected_category = request.args.get("category", "All")

    # build category list
    categories = sorted(set([p[2] for p in results if p[2]]))

    # filter promos
    if selected_category != "All":
        results = [p for p in results if p[2] == selected_category]

    return render_template(
        'promos.html',
        promos=results,
        categories=categories,
        selected_category=selected_category
    )

@promo_routes.route("/promos/search")
def search_promos():
    try:
        query = request.args.get("q", "").lower().strip()
        budget = request.args.get("budget", type=int)
        budget_type = request.args.get("type", "exact")
        pax = request.args.get("pax", type=int)
        
        conn = db_connection()
        cursor = conn.cursor()
        
        params = []
        
        if not query or query in ["all", "all promos", "all items", "show all", "everything", "promos", "items", "menu", "good"]:
            sql = "SELECT * FROM promos WHERE 1=1"
        else:
            sql = """
            SELECT * FROM promos 
            WHERE (
                COALESCE(LOWER(name), '') LIKE %s
                OR COALESCE(LOWER(category), '') LIKE %s
                OR COALESCE(LOWER(description), '') LIKE %s
            )
            """
            params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
            
        # Apply budget filter if provided
        if budget:
            if budget_type == "above":
                sql += " AND price >= %s"
            else:
                sql += " AND price <= %s"
            params.append(budget)
            
        # Apply Pax / Serving Size Filter cleanly as integer match
        if pax:
            sql += " AND serving_size = %s"
            params.append(pax)
            
        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        promos = [dict(zip(columns, row)) for row in rows]
        
        cursor.close()
        conn.close()
        return jsonify(promos)
        
    except Exception as e:
        print("SEARCH ERROR:", e)
        return jsonify({"error": str(e)}), 500


@promo_routes.route("/promos/items/search")
def search_by_items():
    query = request.args.get("q", "").lower().strip()
    budget = request.args.get("budget", type=int)
    budget_type = request.args.get("type", "exact")
    pax = request.args.get("pax", type=int)
    
    print(f"Items search - Query: '{query}', Budget: {budget}, Type: {budget_type}, Pax: {pax}")
    
    conn = db_connection()
    cursor = conn.cursor()
    
    params = []
    
    # If query is completely empty or contains leftover fluff adjectives, treat it as a broad item query
    if not query or query in ["good", "for", "people", "all", "meals", "meal"]:
        sql = "SELECT * FROM promos WHERE 1=1"
    else:
        words = query.split()
        conditions = []
        
        for word in words:
            if len(word) > 1:
                conditions.append("(LOWER(name) LIKE %s OR LOWER(category) LIKE %s)")
                search_pattern = f"%{word}%"
                params.extend([search_pattern, search_pattern])
        
        if conditions:
            # 💡 CHANGED FROM 'OR' JOIN INSIDE AN 'AND' TO ALLOW FLEXIBLE MATCHES
            sql = f"SELECT * FROM promos WHERE ({' OR '.join(conditions)})"
        else:
            sql = "SELECT * FROM promos WHERE LOWER(name) LIKE %s"
            params.append(f"%{query}%")
    
    # Add budget filter if provided
    if budget is not None:
        if budget_type == "above":
            sql += " AND price >= %s"
        else:
            sql += " AND price <= %s"
        params.append(budget)
    
    # Add Pax / Serving Size Filter
    if pax:
        sql += " AND serving_size = %s"
        params.append(pax)
    
    print(f"SQL: {sql}")
    print(f"Params: {params}")
    
    cursor.execute(sql, tuple(params))
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    promos = [dict(zip(columns, row)) for row in rows]
    
    cursor.close()
    conn.close()
    
    return jsonify(promos)

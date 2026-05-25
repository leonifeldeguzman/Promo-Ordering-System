from database.db_connection import conn

def get_promos_by_budget(budget):
    cursor = conn.cursor()
    query = "SELECT * FROM promos WHERE price <= %s"
    cursor.execute(query, (budget,))
    promos = cursor.fetchall()
    return promos

def get_promos_by_category(category):
    cursor = conn.cursor()
    query = "SELECT * FROM promos WHERE LOWER(category) = LOWER(%s)"
    cursor.execute(query, (category,))
    promos = cursor.fetchall()
    return promos

def get_all_promos():
    cursor = conn.cursor()
    query = """
        SELECT id, name, category, price, description, promo_details, status, image_url
        FROM promos
    """
    cursor.execute(query)
    promos = cursor.fetchall()
    return promos

def get_promos_by_category_and_budget(category, budget):

    cursor = conn.cursor()

    query = """
        SELECT * FROM promos
        WHERE LOWER(category) = LOWER(%s)
        AND price <= %s
    """

    cursor.execute(query, (category, budget))

    promos = cursor.fetchall()

    return promos

def add_menu_item(name, price, category, promo_details, status, image_url):
    cursor = conn.cursor()
    
    query = """
        INSERT INTO promos
        (name, price, category, description, promo_details, status, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # Create a description 
    description = f"Delicious {name} promo! Save big on this tasty offer."
    
    cursor.execute(query, (
        name,
        price,
        category,
        description,  # Add this field
        promo_details,
        status,
        image_url
    ))
    
    conn.commit()


def update_price(item_id, new_price):

    cursor = conn.cursor()

    query = """
        UPDATE promos
        SET price = %s
        WHERE id = %s
    """

    cursor.execute(query, (new_price, item_id))

    conn.commit()


def update_status(item_id, status):

    cursor = conn.cursor()

    query = """
        UPDATE promos
        SET status = %s
        WHERE id = %s
    """

    cursor.execute(query, (status, item_id))

    conn.commit()


def delete_menu_item(item_id):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM promos WHERE id = %s", (item_id,))

    conn.commit()
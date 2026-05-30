
from database.db_connection import db_connection


def get_promos_by_budget(budget):

    conn = db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM promos WHERE price <= %s"

    cursor.execute(query, (budget,))
    promos = cursor.fetchall()

    cursor.close()
    conn.close()

    return promos


def get_promos_by_category(category):

    conn = db_connection()
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM promos
    WHERE LOWER(category) LIKE LOWER(%s)
    """

    cursor.execute(query, (f"%{category}%",))
    promos = cursor.fetchall()

    cursor.close()
    conn.close()

    return promos


def get_all_promos():

    conn = db_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, name, category, price, description, promo_details, status, image_url, serving_size
        FROM promos
    """

    cursor.execute(query)
    promos = cursor.fetchall()

    cursor.close()
    conn.close()

    return promos


def get_promos_by_category_and_budget(category, budget):

    conn = db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM promos
        WHERE LOWER(category) = LOWER(%s)
        AND price <= %s
    """

    cursor.execute(query, (category, budget))
    promos = cursor.fetchall()

    cursor.close()
    conn.close()

    return promos


def add_menu_item(name, price, category, promo_details, status, image_url,serving_size):

    conn = db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO promos
        (name, price, category, description, promo_details, status, image_url, serving_size)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    description = f"Delicious {name} promo! Save big on this tasty offer."

    cursor.execute(query, (
        name,
        price,
        category,
        description,
        promo_details,
        status,
        image_url,
        serving_size
    ))

    conn.commit()

    cursor.close()
    conn.close()


def update_price(item_id, new_price):

    conn = db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE promos
        SET price = %s
        WHERE id = %s
    """

    cursor.execute(query, (new_price, item_id))

    conn.commit()

    cursor.close()
    conn.close()


def update_status(item_id, status):

    conn = db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE promos
        SET status = %s
        WHERE id = %s
    """

    cursor.execute(query, (status, item_id))

    conn.commit()

    cursor.close()
    conn.close()


def delete_menu_item(item_id):

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM promos WHERE id = %s",
        (item_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()


def update_item_details(
    item_id,
    item_name,
    category,
    price,
    promo_details,
    status,
    serving_size
):

    conn = db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE promos
        SET
            name = %s,
            category = %s,
            price = %s,
            promo_details = %s,
            status = %s,
            serving_size = %s
        WHERE id = %s
    """

    cursor.execute(query, (
        item_name,
        category,
        price,
        promo_details,
        status,
        serving_size,
        item_id
    ))

    conn.commit()

    cursor.close()
    conn.close()
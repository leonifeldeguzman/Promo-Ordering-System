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
    query = "SELECT * FROM promos"
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
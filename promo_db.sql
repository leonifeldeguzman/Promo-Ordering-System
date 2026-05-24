CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    category VARCHAR(100),
    promo_details TEXT,
    status VARCHAR(50) DEFAULT 'Active'
);
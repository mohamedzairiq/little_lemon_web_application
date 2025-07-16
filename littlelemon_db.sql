-- Create the database
CREATE DATABASE IF NOT EXISTS littlelemon_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE littlelemon_db;

-- Booking table
CREATE TABLE restaurant_booking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    guest_number INT,
    comment VARCHAR(1000)
);

-- Category table
CREATE TABLE restaurant_category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slug VARCHAR(255),
    title VARCHAR(255)
);

-- Menu table
CREATE TABLE restaurant_menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200),
    price INT,
    description VARCHAR(1000),
    category_id INT,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES restaurant_category(id) ON DELETE RESTRICT
);

-- Cart table
CREATE TABLE restaurant_cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    menuitem_id INT,
    quantity INT,
    unit_price DECIMAL(6,2),
    price DECIMAL(6,2),
    CONSTRAINT fk_user_cart FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_menuitem_cart FOREIGN KEY (menuitem_id) REFERENCES restaurant_menu(id) ON DELETE CASCADE
);

-- Order table
CREATE TABLE restaurant_order (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    delivery_crew_id INT NULL,
    status BOOLEAN DEFAULT FALSE,
    total DECIMAL(6,2),
    date DATE,
    CONSTRAINT fk_user_order FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_delivery_crew FOREIGN KEY (delivery_crew_id) REFERENCES auth_user(id)
);

-- OrderItem table
CREATE TABLE restaurant_orderitem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    menuitem_id INT,
    quantity INT,
    unit_price DECIMAL(6,2),
    price DECIMAL(6,2),
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES restaurant_order(id) ON DELETE CASCADE,
    CONSTRAINT fk_menuitem_order FOREIGN KEY (menuitem_id) REFERENCES restaurant_menu(id)
);

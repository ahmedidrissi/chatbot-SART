CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(255),
    description TEXT,
    quantity INT,
    material VARCHAR(255),
    brand VARCHAR(255),
    price DECIMAL(10, 2)
);

CREATE TABLE product_colors (
  id INT PRIMARY KEY,
  product_id INT,
  color VARCHAR(255),
  color_quantity INT,
  FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE sizes (
  id INT PRIMARY KEY,
  product_id INT,
  color_id INT,
  size VARCHAR(50),
  size_quantity INT,
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (color_id) REFERENCES product_colors(id)
);

INSERT INTO products (id, name, category, description, quantity, material, brand, price)
VALUES 
    (1, 'Slim Fit Jeans', 'Jeans', 'A classic pair of slim fit jeans with a modern twist. Made with high-quality denim and designed for a comfortable fit.', 20, 'Denim', 'Zara', 79.99),
    (2, 'Skinny Jeans', 'Jeans', 'Trendy skinny jeans that hug your curves. Perfect for a stylish and sleek look.', 15, 'Denim', 'H&M', 49.99),
    (3, 'Bootcut Jeans', 'Jeans', 'Timeless bootcut jeans that flatter any body shape. Crafted with stretch denim for all-day comfort.', 10, 'Denim', 'Wrangler', 89.99),
    (4, 'Leather Biker Jacket', 'Jackets', 'A classic leather biker jacket that exudes timeless style and attitude. Made from genuine leather for durability.', 10, 'Leather', 'Schott NYC', 199.99),
    (5, 'Denim Jacket', 'Jackets', 'A versatile denim jacket that adds a cool and casual touch to any outfit. Features a button-up front and multiple pockets.', 15, 'Denim', 'Zara', 89.99),
    (6, 'Bomber Jacket', 'Jackets', 'A stylish bomber jacket that combines fashion and functionality. Features a ribbed collar, cuffs, and hem for a comfortable fit.', 12, 'Polyester', 'Alpha Industries', 129.99),
    (7, 'Button-Up Oxford Shirt', 'Shirts', 'A classic button-up Oxford shirt that offers a timeless and polished look. Made from high-quality cotton for comfort and durability.', 20, 'Cotton', 'Brooks Brothers', 79.99),
    (8, 'Flannel Plaid Shirt', 'Shirts', 'A cozy flannel plaid shirt perfect for a casual and laid-back style. Features a soft and warm fabric for chilly days.', 15, 'Flannel', 'L.L.Bean', 59.99),
    (9, 'Printed Graphic T-Shirt', 'Shirts', 'A trendy printed graphic T-shirt that adds a pop of personality to your outfit. Made from soft and breathable cotton.', 10, 'Cotton', 'Urban Outfitters', 29.99),
    (10, 'Wool Blend Overcoat', 'Coats', 'A sophisticated wool blend overcoat that keeps you warm and stylish during colder months. Features a tailored fit and a classic design.', 10, 'Wool Blend', 'Calvin Klein', 249.99),
    (11, 'Parka Jacket', 'Coats', 'A versatile parka jacket designed for extreme weather conditions. Equipped with a hood, insulation, and waterproof features.', 15, 'Nylon', 'Canada Goose', 599.99),
    (12, 'Trench Coat', 'Coats', 'A timeless trench coat that adds elegance to any outfit. Made from durable and water-resistant fabric with a belted waist.', 8, 'Cotton', 'Burberry', 899.99);

INSERT INTO colors (id, product_id, color, color_quantity)
VALUES
  (1, 1, 'Blue', 12),
  (2, 1, 'Black', 8),

  (3, 2, 'White', 5),
  (4, 2, 'Gray', 10),

  (5, 3, 'Indigo', 5),
  (6, 3, 'Dark Blue', 5),

  (7, 4, 'Black', 4),
  (8, 4, 'Brown', 6),

  (9, 5, 'Light Blue', 8),
  (10, 5, 'Medium Blue', 7),

  (11, 6, 'Green', 5),
  (12, 6, 'Black', 7),

  (13, 7, 'White', 10),
  (14, 7, 'Blue', 10),

  (15, 8, 'Red', 6),
  (16, 8, 'Green', 9),

  (17, 9, 'Black', 5),
  (18, 9, 'Gray', 5),

  (19, 10, 'Black', 7),
  (20, 10, 'Charcoal', 3),

  (21, 11, 'Navy', 5),
  (22, 11, 'Black', 10),

  (23, 12, 'Beige', 3),
  (24, 12, 'Khaki', 5);

INSERT INTO sizes (id, product_id, color_id, size, size_quantity)
VALUES
  (1, 1, 1, 'S', 6),
  (2, 1, 1, 'L', 6),
  (3, 1, 2, 'M', 4),
  (4, 1, 2, 'XL', 4),

  (5, 2, 3, 'S', 3),
  (6, 2, 3, 'L', 2),
  (7, 2, 4, 'M', 5),
  (8, 2, 4, 'XL', 5),

  (9, 3, 5, 'S', 2),
  (10, 3, 5, 'L', 3),
  (11, 3, 6, 'M', 3),
  (12, 3, 6, 'XL', 2),

  (13, 4, 7, 'S', 2),
  (14, 4, 7, 'L', 2),
  (15, 4, 8, 'M', 4),
  (16, 4, 8, 'XL', 2),

  (17, 5, 9, 'S', 6),
  (18, 5, 9, 'L', 2),
  (19, 5, 10, 'M', 3),
  (20, 5, 10, 'XL', 4),

  (21, 6, 11, 'S', 2),
  (22, 6, 11, 'L', 3),
  (23, 6, 12, 'M', 4),
  (24, 6, 12, 'XL', 3),

  (25, 7, 13, 'S', 4),
  (26, 7, 13, 'L', 6),
  (27, 7, 14, 'M', 6),
  (28, 7, 14, 'XL', 4),

  (29, 8, 15, 'S', 3),
  (30, 8, 15, 'L', 3),
  (31, 8, 16, 'M', 5),
  (32, 8, 16, 'XL', 4),

  (33, 9, 17, 'S', 3),
  (34, 9, 17, 'L', 2),
  (35, 9, 18, 'M', 4),
  (36, 9, 18, 'XL', 3),

  (37, 10, 19, 'S', 3),
  (38, 10, 19, 'L', 4),
  (39, 10, 20, 'M', 1),
  (40, 10, 20, 'XL', 2),

  (41, 11, 21, 'S', 2),
  (42, 11, 21, 'L', 3),
  (43, 11, 22, 'M', 4),
  (44, 11, 22, 'XL', 6),

  (45, 12, 23, 'S', 1),
  (46, 12, 23, 'L', 2),
  (47, 12, 24, 'M', 3),
  (48, 12, 24, 'XL', 2);

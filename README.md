# Grocery Store Application V1
## Description
The objective of the Modern Application Development - I project is to develop a robust and user-friendly online grocery shopping platform that enables users to search and purchase groceries categorised for easy navigation providing a seamless and convenient way to shop for groceries online.
## Technologies used
The following Technologies have been used in implementing the web application:
### Python
Python is a programming language which is used for backend development.
### Flask
Flask is a web framework for Python which is used to build the application quickly and efficiently.
### Flask-SQLAlchemy
Flask-SQLAlchemy is a database toolkit for Flask web applications which is used to conveniently interact with the SQLite3 databases for the application.
### Jinja2
Jinja2 is a templating engine for Python which is used to generate dynamic web content using templates for the application.
### Bootstrap
Bootstrap is a frontend framework which is used to design the application.
### SQLite3
SQLite3 is a SQL database management system which is used to store the data of the application.
### Matplotlib
Matplotlib is a plotting library for Python which is used to visualise the data in the admin dashboard of the application.

## DB Schema Design
The following tables are used to store the data for the web application:

### The User table contains the following attributes:

userid - integer, auto increment, primary key.

username - string, unique, not null.

password - string, not null.

isadmin - integer, not null, default = 0, stores 1 when the user is an admin.

cart - relationship with Cart table. Easy access to the cart data of the user.

### The Category table contains the following attributes:

categoryid - integer, auto increment, primary key.

categoryname - string, unique, not null.

products - relationship with Product table. Easy access to the product data of the category.

### The Product table contains the following attributes:

productid - integer, auto increment, primary key.

productname - string, not null.

price - float, not null.

quantity - integer, not null.

categoryid - foreign key for categoryid of Category table, not null.

cart - relationship with Cart table. Easy access to the cart data of the product.

### The Cart table contains the following attributes:

cartid - integer, auto increment, primary key.

userid - foreign key for userid of User table, not null.

productid - foreign key for productid of Product table, not null.

quantity - integer, not null.

buy - integer, not null, default = 0, stores 1 when the user purchases the product.


## Architecture and Features
The project exhibits a well-defined organisational structure. This includes GrocerStore.py, readme.txt, requirements.txt, local_setup.sh, and local_run.sh files, alongside the application, controllers, db_directory, static, and templates folders. Notably, the application folder contains config.py, database.py, and models.py files, which manage critical configuration and database aspects. Furthermore, the controllers folder is organised into controller, admin_controller, and user_controller, which contains the controllers employed in the applications backend. Additionally, the db_directory stores the application's database, while the static folder contains images utilised throughout the project. Finally, the templates folder contains HTML templates employed in the application's interface.

The project is implemented with comprehensive features, catering to both user and administrative needs. A dedicated login page enables seamless access for registered users, while a separate register page allows new users to join. The user-friendly interface permits customers to effortlessly browse products organised into categories or utilise a robust search function to find specific items. Detailed product pages display vital information, such as prices and availability, and allow users to efficiently add items to their cart. The shopping cart provides an extensive overview of selected products, including the total amount, fostering informed purchasing decisions. Purchased products are conveniently displayed within each user's profile. On the administrative side, the project offers valuable insights through visual representations of categories, products, unavailable stock, top-selling items, and website statistics. Additionally, admins can efficiently manage inventory by adding, updating, and deleting categories and products as needed.

## Video
https://drive.google.com/file/d/1UcHfq-8ls2To6K2xxre-tTkliMQBWBR6/view?usp=sharing

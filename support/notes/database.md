# Databases

## mysql
app.py
```python
app.app_context().push()
```

terminal
```bash
# Install MySQL Server
(virt)$ sudo apt install mysql-server
(virt)$ systemctl status mysql

# Create MySQL User & Password
(virt)$ sudo mysql --user=root mysql
mysql> CREATE USER 'db-admin'@'localhost' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'db-admin'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> quit;
(virt)$ sudo systemctl restart mysql
(virt)$ python3 support/create_db.py --task create

# Initialize MySQL Database for Flask usage
(virt)$ pip install pymysql
(virt)$ pip install cryptography
(virt)$ python3
>>> from app import app
>>> from app import db
>>> db.create_all()
>>> quit()

# Login as MySQL User and Show Data
### http://g2pc1.bu.edu/~qzpeng/manual/MySQL%20Commands.htm
(virt)$ mysql -u <db-admin or db-user> -p
(passwd) password
mysql> SHOW DATABASES;
mysql> USE tenants;
mysql> SHOW TABLES;
mysql> EXPLAIN users;
mysql> SELECT * FROM users;
mysql> EXPLAIN posts;
mysql> SELECT * FROM posts;
mysql> quit;

# Delete Records from Users (or Posts) Tables
mysql> DELETE FROM users WHERE username = "jward";

# Change User ID of User in `users` Table
mysql> UPDATE users SET id = 1 WHERE username = "jward";
mysql> SELECT id, username FROM users;

# Delete 'users' Table
mysql> DELETE FROM users;

# Migration (add/remove columns to Database)
(virt)$ pip install Flask-Migrate
(virt)$ flask db init
(virt)$ flask db migrate -m 'Initial Migration'
(virt)$ flask db upgrade

# Other Flask Migration Commands
(virt)$ flask db help
(virt)$ flask db stamp head          # Fix for 'Target database is not up to date'
(virt)$ flask db history
(virt)$ flask db check               # Check if there are any new operations to migrate

```
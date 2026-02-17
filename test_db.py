from db_config import db

if db.is_connected():
    print("Database connected successfully!")
else:
    print("Connection failed")

from __init__ import *

import shelve

with shelve.open('storage.db') as db:
    users = db.get('Users', {})
    for user_id, user in users.items():
        print(f"User ID: {user_id}")
        print(f"Username: {user.get_username()}")
        print(f"Email: {user.get_email()}")
        print(f"Password: {user.get_password()}")
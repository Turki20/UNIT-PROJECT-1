from database.models import User
from database.db import execute, get_all, clost_db


print()

def check_user_exist(username, password):
    all = get_all(User.get_all_users_query())
    users = User.convert_to_Users(all)
    
    for user in users:
        if user.username == username and user.password == password:
            return user
    
    return None
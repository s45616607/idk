from pymongo import MongoClient
from datetime import datetime, timezone
from configs import cfg
import random

cl = MongoClient(cfg.MONGO_URI)
users_ban = cl['main']['users_ban']
users = cl['main']['users']
Referrals = cl["main"]['Referrals']


#---------------help methods ---------
def makeKey():
    for i in range(10):
        key = ""
        for j in range(10):
            key += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    return key;




# --------------- Ban commands -----------
def already_ban(user_id):
    user = users_ban.find_one({"user_id" : str(user_id)})
    if not user:
        return False
    return True

def ban_user(user_id):
    in_db = already_ban(user_id)
    if in_db:
        return
    return users_ban.insert_one({"user_id": str(user_id)}) 
def unban_user(user_id):
    return users_ban.delete_one({"user_id": str(user_id)})




#---------------LANG------------------
def get_user_lang(user_id: int) -> str:
    user = users.find_one({"user_id": user_id})
    if user and "lang" in user:
        return user["lang"]
    return None


#-----------users-------------------------
def save_user(username:str, user_id: int):
    user_data = {
        "chat_id": user_id,
        "username": username.lower() if username else None,
        "stars": 0,
        "date_joined": datetime.now().strftime("%Y-%m-%d %I:%M:%S"),
        "ref": makeKey()
        
    }
    try:
        users.update_one({"id": str(user_id)}, {"$set": user_data}, upsert=True)
        print(f"✅ User {user_id} saved.")
    except Exception as e:
        print(f"⚠️ User {user_id} already exists or error: {e}")

def user_exists(user_id: int) -> bool:
    user = users.find_one({
        "id": str(user_id),
    })
    return user is not None

def total_users():
    total_users = users.count_documents({})
    return total_users


#-------------- REFERRAL --------------------------------------
def register_referral(new_user_id: int, referrer_id: int):
    if Referrals.find_one({"user_id": new_user_id}):
        return  # لا تسجل إذا كان موجود مسبقاً

    Referrals.insert_one({
        "user_id": new_user_id,
        "referrer_id": referrer_id,
        "joined_at": datetime.now(timezone.utc)
    })
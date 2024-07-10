from models.user_models.user import User as UserModel
from database.connection import user_collection
from bson import ObjectId






class UserRepository:
    @staticmethod
    async def get_all(query):
        try:
            return user_collection.find(query)
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None

    @staticmethod
    async def get(id):
        try:
            return user_collection.find_one({"_id": ObjectId(id)})
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None

    @staticmethod
    async def get_by_username(username):
        try:
            user = user_collection.find_one({"username": username})
            if user:
                return UserModel(**user)
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None

    @staticmethod
    async def set(user):
        try:
            user = user_collection.insert_one(user)
            return user.inserted_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    async def edit(id, update):
        try:
            return user_collection.find_one_and_update(
                {"_id": ObjectId(id)}, {"$set": update}, return_document=True
            )
        except Exception as e:
            print(f"Error updating user: {e}")
            return None

    @staticmethod
    async def delete(id):
        try:
            return user_collection.find_one_and_delete({"_id": ObjectId(id)})
        except Exception as e:
            print(f"Error deleting user: {e}")
            return None

    @staticmethod
    async def check_existing_user(user):
        try:
            existing_user = user_collection.find_one(
                {"$or": [{"username": user.username}, {"email": user.email}]}
            )
            if existing_user:
                return {"message": "Username or email already exists"}
        except Exception as e:
            print(f"Error checking user data: {e}")
            return None

    @staticmethod
    async def remove_user_from_all_friends_lists(user_id):
        try:
            user_collection.update_many(
                {"friends": user_id}, {"$pull": {"friends": user_id}}
            )
        except Exception as e:
            print(f"An error occurred while removing user from friends lists: {e}")

    @staticmethod
    async def apply_document_id_to_user(document_id, user_id, attribute):
        try:
            return user_collection.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$push": {attribute: str(document_id)}},
                return_document=True,
            )
        except Exception as e:
            print(f"An error occurred while applying document id to user: {e}")
            return None

    @staticmethod
    async def delete_document_id_from_user(document_id, user_id, attribute):
        try:
            return user_collection.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$pull": {attribute: str(document_id)}},
                return_document=True,
            )
        except Exception as e:
            print(f"An error occurred while removing document id from user: {e}")
            return None

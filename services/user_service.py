from bson import ObjectId
from fastapi import HTTPException
from repositories.user_repository import UserRepository
from models.user_models.user import User as UserModel
from services.security_service import SecurityService


class UserService:
    @staticmethod
    async def map_document_to_user(document_id, user_id, attribute):
        updated_user = await UserRepository.apply_document_id_to_user(
            document_id, user_id, attribute
        )
        if updated_user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

    @staticmethod
    async def remove_document_id_from_user(document_id, user_id, attribute):
        updated_user = await UserRepository.delete_document_id_from_user(
            document_id, user_id, attribute
        )
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")

    @staticmethod
    async def get_user_by_id(id):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid id")

        user = await UserRepository.get(id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return UserModel(**user)

    @staticmethod
    async def get_all_users(username=None):
        query = {"username": username} if username else {}

        user_data = await UserRepository.get_all(query)

        if user_data is None:
            raise HTTPException(status_code=404, detail="Users not found")
        else:
            users_list = []
            for document in user_data:
                users_list.append(UserModel(**document))
            if len(users_list) > 0:
                return users_list
            else:
                raise HTTPException(status_code=404, detail="Users not found")

    @staticmethod
    async def create_new_user(user):
        existing_user = await UserRepository.check_existing_user(user)
        if existing_user:
            raise HTTPException(status_code=409, detail=existing_user)

        hashed_password = SecurityService.get_password_hash(user.password)
        user_dict = user.dict(exclude={"password"})
        user_dict["hashed_password"] = hashed_password
        user_dict["workouts"] = []
        user_dict["nutrition"] = []
        user_dict["friends"] = []
        user_dict["disabled"] = False

        inserted_id = await UserRepository.set(user_dict)

        if inserted_id is None:
            return None
        else:
            return UserModel(**{**user_dict, "id": inserted_id})

    @staticmethod
    async def edit_user_data(id, update, current_user):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid id")
        if id != current_user.id:
            raise HTTPException(status_code=401, detail="Cannot edit other users")

        update_dict = dict(update)

        updated_user = await UserRepository.edit(id, update_dict)

        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return UserModel(**updated_user)

    @staticmethod
    async def remove_user_data(id, current_user):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid id")
        if id != current_user.id:
            raise HTTPException(status_code=401, detail="Cannot delete other users")

        deleted_user = await UserRepository.delete(id)
        await UserRepository.remove_user_from_all_friends_lists(id)

        if deleted_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return UserModel(**deleted_user)

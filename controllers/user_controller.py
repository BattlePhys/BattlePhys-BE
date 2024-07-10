from repositories.user_repository import UserRepository
from services.user_service import UserService


class UserController:
    @staticmethod
    async def get_all_users(username=None):
        users = await UserService.get_all_users(username)
        return users

    @staticmethod
    async def get_by_id(id):
        user = await UserService.get_user_by_id(id)
        return user

    @staticmethod
    async def post_user(user):
        new_user = await UserService.create_new_user(user)
        return new_user

    @staticmethod
    async def update_user(id, update, current_user):
        updated_user = await UserService.edit_user_data(id, update, current_user)
        return updated_user

    @staticmethod
    async def delete_user(id, current_user):
        deleted_user = await UserService.remove_user_data(id, current_user)
        return deleted_user

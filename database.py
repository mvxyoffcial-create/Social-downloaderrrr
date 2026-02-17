import motor.motor_asyncio
from config import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users = self.db['users']
        self.broadcast = self.db['broadcast']

    async def add_user(self, user_id, first_name, last_name, username):
        """Add a new user to the database"""
        user_data = {
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'username': username
        }
        
        existing_user = await self.users.find_one({'user_id': user_id})
        if not existing_user:
            await self.users.insert_one(user_data)
            return True
        else:
            await self.users.update_one({'user_id': user_id}, {'$set': user_data})
            return False

    async def get_all_users(self):
        """Get all user IDs from database"""
        users = []
        async for user in self.users.find():
            users.append(user['user_id'])
        return users

    async def total_users_count(self):
        """Get total user count"""
        count = await self.users.count_documents({})
        return count

    async def delete_user(self, user_id):
        """Delete a user from database"""
        await self.users.delete_one({'user_id': user_id})

    async def is_user_exist(self, user_id):
        """Check if user exists in database"""
        user = await self.users.find_one({'user_id': user_id})
        return True if user else False

# Initialize database
db = Database(Config.DATABASE_URI, Config.DATABASE_NAME)

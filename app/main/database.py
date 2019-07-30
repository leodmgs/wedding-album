import pymongo
from bcrypt import hashpw


class DB(object):
    URI = "mongodb://127.0.0.1:27017"

    @staticmethod
    def init():
        client = pymongo.MongoClient(DB.URI)
        DB.DATABASE = client['wedding_gallery_db']

    @staticmethod
    def insert(collection, data):
        return DB.DATABASE[collection].insert_one(data)

    @staticmethod
    def generate_numbers_test(collection):
        for i in range(1, 100):
            DB.DATABASE[collection].insert_one({'number': i})

    @staticmethod
    def collection(collection):
        return DB.DATABASE[collection]

    @staticmethod
    def find(collection, query):
        return DB.DATABASE[collection].find(query)

    @staticmethod
    def find_limit(collection, query, limit):
        return DB.DATABASE[collection].find(query).limit(limit)

    @staticmethod
    def find_sort_limit(collection, query, sort, limit):
        return DB.DATABASE[collection].find(query).sort(sort).limit(limit)

    @staticmethod
    def validate(collection, query):
        local_user = DB.DATABASE[collection].find_one({'email': query['email']})
        if local_user:
            hashpass = hashpw(query['password'].encode('utf-8'), local_user['password'])
            if local_user['password'] == hashpass:
                return True, local_user['_id']
            else:
                return False, "invalid password!"
        return False, "user not found!"

    @staticmethod
    def update(collection, query, update):
        result = DB.DATABASE[collection].update_one(query, update, upsert=False)
        if result.modified_count == 1:
            return True
        return False

    @staticmethod
    def delete(collection, query):
        result = DB.DATABASE[collection].delete_one(query)
        if result.deleted_count == 1:
            return True
        return False

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask import flash
import re
from flask_app import BCRYPT
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date = data['date']
        self.how_many = data['how_many']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM  sightings LEFT JOIN users ON sightings.user_id = users.id;"
        sightings = []
        results = connectToMySQL('sightings_db').query_db(query)
        print(results)
        for row in results:
            sighting = cls(row)
            user_data = {
                **row, 
                "id": row["users.id"],
                "created_at" : row["users.created_at"],
                "updated_at" : row['users.updated_at']
            }
            new_user = user_model.User(user_data)
            sighting.user = new_user 
            sightings.append(sighting)
        return sightings
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO sightings (location, what_happened, date, how_many, created_at, updated_at, user_id) VALUES( %(location)s, %(what_happened)s, %(date)s, %(how_many)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL('sightings_db').query_db(query,data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE sightings SET location=%(location)s, what_happened=%(what_happened)s, date=%(date)s, how_many=%(how_many)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('sightings_db').query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM sightings WHERE id = %(id)s"
        return connectToMySQL('sightings_db').query_db(query,data)
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        result = connectToMySQL('sightings_db').query_db(query,data)
        return cls(result[0])
    

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM  sightings LEFT JOIN users ON sightings.user_id = users.id WHERE sightings.id = %(id)s;"
        results = connectToMySQL('sightings_db').query_db(query,data)
        print(results)
        sighting = cls(results[0])
        user_data = {
            **results[0], 
            "id": results[0]["users.id"],
            "created_at" : results[0]["created_at"],
            "updated_at" : results[0]['updated_at']
        }
        new_user = user_model.User(user_data)
        sighting.user = new_user 
        return sighting
    
    @staticmethod
    def validate_sighting(data):
        print(data)
        is_valid = True

        if data['location'] == '':
            flash("All fields required!")
            is_valid = False

        if data['what_happened'] == '':
            flash("All fields required!")
            is_valid = False

        if data['date'] == '':
            flash("All fields required!")
            is_valid = False

        if data['how_many'] == '':
            flash("All fields required!")
            is_valid = False

        if data['how_many'] != '': 
            if int(data['how_many']) < 1:
                flash("# of Sasquatches must be more than 1!")
                is_valid = False

        return is_valid
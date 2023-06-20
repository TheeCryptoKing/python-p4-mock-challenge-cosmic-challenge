#Vahans Code 

# models.py:
# 11:18
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData, UniqueConstraint, DateTime
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin
# convention = {
#     "ix": "ix_%(column_0_label)s",
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(constraint_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s",
# }
# metadata = MetaData(naming_convention=convention)
# db = SQLAlchemy(metadata=metadata)
# class Planet(db.Model, SerializerMixin):
#     __tablename__ = 'planets'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     distance_from_earth = db.Column(db.String)
#     nearest_star = db.Column(db.String)
#     image = db.Column(db.String)
#     # created_at = db.Column(db.DateTime, db.func.now())
#     # updated_at = db.Column(db.DateTime, db.func.now())
#     planet_missions = db.relationship("Mission", back_populates="planet")
#     scientist = association_proxy("planet_missions", "scientist")
#     serialize_only = (
#         "id",
#         "name",
#         "distance_from_earth",
#         "nearest_star",
#         "image",
#     )
# class Scientist(db.Model, SerializerMixin):
#     __tablename__ = 'scientists'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False, unique=True)
#     field_of_study = db.Column(db.String, nullable=False)
#     avatar = db.Column(db.String)
#     # created_at = db.Column(db.DateTime, db.func.now())
#     # updated_at = db.Column(db.DateTime, db.func.now())
#     scientist_missions = db.relationship("Mission", back_populates="scientist")
#     planets = association_proxy("scientist_missions", "planet")
#     serialize_only = (
#         "id",
#         "name",
#         "field_of_study",
#         "avatar",
#     )
#     @validates("name")
#     def validates_name(self, key, name):
#         if not name or len(name) < 1:
#             raise ValueError("Invalid name")
#         return name
#     @validates("field_of_study")
#     def validates_field_of_study(self, key, field_of_study):
#         if not field_of_study or len(field_of_study) < 1:
#             raise ValueError("Invalid field")
#         return field_of_study
# class Mission(db.Model, SerializerMixin):
#     __tablename__ = 'missions'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     # created_at = db.Column(db.DateTime, db.func.now())
#     # updated_at = db.Column(db.DateTime, db.func.now())
#     scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id"), nullable=False)
#     planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=False)
#     scientist = db.relationship("Scientist", back_populates="scientist_missions")
#     planet = db.relationship("Planet", back_populates="planet_missions")
#     serialize_only = (
#         "id",
#         "name",
#         "scientist_id",
#         "planet_id",
#     )
#     @validates("name")
#     def validates_name(self, key, name):
#         if not name or len(name) < 1:
#             raise ValueError("Invalid name")
#         return name
#     @validates("scientist_id")
#     def validates_scientist_id(self, key, scientist_id):
#         if not scientist_id:
#             raise ValueError("Invalid scientist_id")
#         return scientist_id
#     @validates("planet_id")
#     def validates_planet_id(self, key, planet_id):
#         if not planet_id:
#             raise ValueError("Invalid planet_id")
#         return planet_id



# app.py:
# 11:18
# from flask import Flask, make_response, jsonify, request
# from flask_migrate import Migrate
# from flask_restful import Api, Resource
# from flask_cors import CORS
# from models import db, Planet, Scientist, Mission
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.json.compact = False
# migrate = Migrate(app, db)
# CORS(app)
# api = Api(app)
# db.init_app(app)
# @app.route('/')
# def home():
#     return ''

# class Scientists(Resource):

# GET 
#     def get(self):
#         scientists = [s.to_dict() for s in Scientist.query.all()]
#         return scientists, 200
# POST 
#     def post(self):
#         data = request.get_json()
#         try:
#             new_scientist = Scientist(
#                 name = data.get("name"),
#                 field_of_study = data.get("field_of_study"),
#                 avatar = data.get("avatar"),
#             )
#             db.session.add(new_scientist)
#             db.session.commit()
#             return new_scientist.to_dict(), 201
#         except Exception:
#             return ({"error": "400: Validation error"}, 400)
# api.add_resource(Scientists, "/scientists")

# class ScientistById(Resource):
# GET 
#     def get(self, id):
#         try:
#             scientist = Scientist.query.filter(Scientist.id == id).first()
#             return scientist.to_dict(), 200
#         except Exception:
#             return ({"error": "400: Validation error"}, 400)
# PATCH
#     def patch(self, id):
#         data = request.get_json()
#         scientist = Scientist.query.filter(Scientist.id == id).first()
#         if not scientist:
#             return ({"error": "404 not found"}, 404)
#         for attr in data:
#             setattr(scientist, attr, data.get(attr))
#         db.session.add(scientist)
#         db.session.commit()
#         return scientist.to_dict(), 202
# DELETE
#     def delete(self, id):
#         scientist = Scientist.query.filter_by(id = id).first()
#         missions = Mission.query.filter_by(id = id).all()
#         if not scientist:
#             return ({"error": "404 not found"}, 404)
#         if missions:
#             for m in missions:
#                 db.session.query(Mission).filter(Mission.id == m.id).delete()
#                 db.session.commit()
#         db.session.delete(scientist)
#         db.session.commit()
#         return ({}, 204)
# api.add_resource(ScientistById, "/scientists/<int:id>")

# class Missions(Resource):
# GET
#     def post(self):
#         data = request.get_json()
#         try:
#             new_mission = Mission(
#                 name = data.get('name'),
#                 scientist_id = data.get('scientist_id'),
#                 planet_id = data.get('planet_id'),
#             )
#             db.session.add(new_mission)
#             db.session.commit()
#             return new_mission.to_dict(), 201
#         except:
#             return "Could not post mission", 400
# api.add_resource(Missions, "/missions")
# if __name__ == '__main__':
#     app.run(port=5555, debug=True)

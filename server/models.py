from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Scientist(db.Model, SerializerMixin):
    __tablename__= 'scientists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    field_of_study = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=False)
    
    scientist_missons = db.relationship('Mission', back_populates='scientist')
    
    planets = association_proxy("scientist_missions", "planet")
    # calling planet from mmissions
    
    # not loading any data 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # @validates('name','field_of_study')
    # def validate_string(self, key, name, field_of_study):
    #     if isinstance(key, str) and len(key) < 1:
    #         raise ValueError('Fix it stupid')
    #     return name, field_of_study
    
    serialize_only = (
        "id",
        "name",
        "field_of_study",
        "avatar"
        )
    
    #  or 
    @validates('name')
    def validate_string(self, key, name):
        if not name or len(name) < 1:
            raise ValueError('Fix it stupid')
        return name

    @validates('field_of_study')
    def validate_string(self, key, field_of_study):
        if not field_of_study or len(field_of_study) < 1:
            raise ValueError('Fix it stupid')
        return field_of_study
    
    # pass


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    distance_from_earth = db.Column(db.String, nullable=False)
    nearest_star = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    
    planet_missions = db.relationship('Mission', back_populates='planet')
    
    scientists = association_proxy("planet_missons", "scientist")
    # association proxy line up with missions from planet
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    serialize_only = (
        "id",
        "name",
        "distance_from_earth",
        "nearest_star",
        "image"
        )

    
    # pass

# Intermediary has to be here??? #Vahan says No 
class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    scientist_id = db.Column(db.Integer, ForeignKey('scientists.id'), nullable=False)
    planet_id = db.Column(db.Integer, ForeignKey('planets.id'), nullable=False)
    
    scientist = db.relationship('Scientist', back_populates='scientist_missons')
    planet = db.relationship('Planet', back_populates='planet_missions')
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    serialize_only = (
        "id",
        "name",
        "scientist_id",
        "planet_id"
        )
    
    @validates('name')
    def validates_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError('Fix the Mission Name')
        return name 
    
    @validates('scientist')
    def validates_scientist(self, key, scientist_id):
        if not scientist_id:
            raise ValueError('Fix scientist_id')
        return scientist_id
    
    @validates('planet')
    def validates_planet(self, key, planet_id):
        if not planet_id:
            raise ValueError('Fix planet_id')
        return planet_id
    
    
    # pass 


# write get post, patch delete for all classes
# practice logic for patching and deleting nested data
# practice validations
# practice seriale_rules


# add any models you may need. 
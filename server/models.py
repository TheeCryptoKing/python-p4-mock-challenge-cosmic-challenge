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


# Nullable and Validates makes data safer
class Scientist(db.Model, SerializerMixin):
    __tablename__= 'scientists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    field_of_study = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=False)
    
    # Back population for ForeignKey in scientist table
    scientist_missions = db.relationship('Mission', back_populates='scientist')
    # more exact data transfer for scientists tbale and planet table,     # calling planet from mmissions
    planets = association_proxy("scientist_missions", "planet")
    
    # works with brand new seed
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    # works when updated 
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    
    # Redone with serialize_rules
    # Avoiding max recursion a.k.a infinity loops
    # need visual representaion of tables to see which data is looping
    # Writing only in to_dict() to find which attributes cause max_recursion 
    serialize_rules = (
        "-planets.planet_missions",
        "-scientist_missions.planet",
        "-scientist_missions.scientist"
        )
    
    # Done intially with Only
    # serialize_only = (
    #     "id",
    #     "name",
    #     "field_of_study",
    #     "avatar"
    #     )
    # redone with @validates and name and field_of_study with string 
    
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
    
    # Back population fro ForeignKey in planet table
    planet_missions = db.relationship('Mission', back_populates='planet')
    # association proxy line up with missions from planet
    scientists = association_proxy("planet_missions", "scientist")
    
    # works with brand new seed
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # works when updated 
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Redone with serialize_rules, apparently not needed
    # Need to refrence back population in proper sytntax order with how it calls data and then returns
    serialize_rules = (
        "-planet_missions.planet",
    )
    
    # why do i need only here????
    # Done intially with Only
    # serialize_only = (
    #     "id",
    #     "name",
    #     "distance_from_earth",
    #     "nearest_star",
    #     "image"
    #     )
    
    # pass

# Intermediary has to be here??? #Vahan says No 
class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'
#     __table_args__ = (UniqueConstraint("name", "scientist_id", "planet_id"),)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    scientist_id = db.Column(db.Integer, ForeignKey('scientists.id'), nullable=False)
    planet_id = db.Column(db.Integer, ForeignKey('planets.id'), nullable=False)
    
    scientist = db.relationship('Scientist', back_populates='scientist_missions')
    planet = db.relationship('Planet', back_populates='planet_missions')
    
    # works with brand new seed
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # works when updated 
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Redone with serialize_rules
    serialize_rules = (
        "-scientist.scientist_missions",
        "-planet.planet_missions",
    )
    
    # Done intially with Only
    # serialize_only = (
    #     "id",
    #     "name",
    #     "scientist_id",
    #     "planet_id"
    #     )
    
    @validates('name')
    def validates_name(self, key, name):
        if not name or len(name) < 0:
            raise ValueError('Fix the Mission Name')
        return name 
    
    @validates('scientist')
    def validates_scientist(self, key, scientist_id):
        if scientist_id:
            raise ValueError('Fix scientist_id')
        return scientist_id
    
    @validates('planet')
    def validates_planet(self, key, planet_id):
        if planet_id:
            raise ValueError('Fix planet_id')
        return planet_id
    
    # pass 


# write get post, patch delete for all classes
# practice logic for patching and deleting nested data
# practice validations
# practice seriale_rules

# learned Flask Shell can be typed inside of server 

#Ask micheal why Post isn't working and why need serialize only on Planets,  

# add any models you may need. 
#!/usr/bin/env python3
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Planet, Scientist, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route('/')
def home():
    return ''

# GET /scientists
# POST /scientists

# GET /scientists/int:id
# PATCH /scientists/:id
# DELETE /scientists/int:id

# GET /planets
# add patch, post

# POST /missions
# add patch, delete
class Scientists(Resource):
    def get(self):
        scientists = [s.to_dict() for s in Scientist.query.all()]
        # when returing data can do [m.to_dict(only=('id', 'name', 'field_of_study', 'avatar')) for s in Scientist.query.all()]
        # when using serialzie rules
        
        if scientists:
            return scientists, 200 
        else: 
            # can also import and use abort and replace return with abort(422)
            # make_response only returned if everything works
            return 'Need to fix Scientists GET'
        # Working with serialized data 
        
    def post(self):
        data = request.get_json()
        try:
            new_scientist = Scientist(
                name=data.get("name"),
                field_of_study=data.get('field_of_study'),
                avatar=data.get('avatar')
            )
            db.session.add(new_scientist)
            db.session.commit()
            return new_scientist.to_dict(), 201
        except:
                return {"error": "400: Validation error"}, 400
        # working
        pass
api.add_resource(Scientists, '/scientists')

class ScientistsId(Resource):
    def get(self, id):
        laddies = Scientist.query.filter_by(id=id).first()
        if laddies:
            return laddies.to_dict(), 200
        else:
            return 'Fix ScientistsId GET '
        # Working serialzie not ordered properly, how do i? 
        # pass 
    
    def patch(self, id):
        data = request.get_json()
        laddies = Scientist.query.filter_by(id=id).first()
        #  dont understand how this works
        if not laddies:
            return ({"error": "404 not found"}, 404)
        else:
            for attr in data:
                setattr(laddies, attr, data.get(attr))
            db.session.add(laddies)
            db.session.commit()
            return laddies.to_dict(), 202
        # working
        
    def delete(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        # vahan method campares mission id w/ current mission id not scientist id
        if scientist:
            Mission.query.filter_by(scientist_id=id).delete()
            db.session.delete(scientist)
            db.session.commit()
            return make_response({}, 204)
        else: 
            return ({"error": "404 not found"}, 404)
        # not working
        # pass
    
api.add_resource(ScientistsId, '/scientists/<int:id>')

class Planets(Resource):
    def get(self):
        planets = [p.to_dict() for p in Planet.query.all()]
        # need if or try for validation 
        return planets, 200 
        # working
        # pass
    
api.add_resource(Planets, '/planets')

class Missions(Resource):
    def get(self):
        missions = [m.to_dict() for m in Mission.query.all()]
        return missions, 200
        # working
        # pass

    
    def post(self):
        data = request.get_json()
        try:
            new_mission = Mission(
                name = data.get('name'),
                scientist_id = data.get('scientist_id'),
                planet_id = data.get('planet_id')
            )
            db.session.add(new_mission)
            db.session.commit()
            # How do i return planet???
            # response = make_response(
            #     planetOfMission = Planet.query.filter(Mission.planet_id == Planet.id)
            # )
            # i do want to know how to retrun plant data from planet_id
            
            return new_mission.to_dict(), 201
        except:
            return {"error": "400: Validation error"}
        # working but need to return planet
        # pass
    
api.add_resource(Missions, '/missions')



if __name__ == '__main__':
    app.run(port=5555, debug=True)





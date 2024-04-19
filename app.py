#!/usr/bin/env python3
from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api
from models.dbmodel import Doctor, Patient, Appointment, Specialization


# Routes

# Sign a user up
class Signup(Resource):

    def post(self):
        # A user is either a doctor or a patient
        json = request.get_json()

        if json['password'] is not json['password']:
            return {"errors" : ["Passwords do not match"]}, 401
        
        if json.get('doctors_id'):
            # Add doctor
            try:
                doctor = Doctor(
                name=json['name'], username=json['username'], email=json['email'], address=json['address'], gender= json['gender'], doctors_id=json['doctors_id'], specialization=json['specialization'])
                doctor.password_hash = json['password']
                db.session.add(doctor)
                db.session.commit()
                # Add session
                session['user_id'] = doctor.id
            except IntegrityError as e:
                error_msg = str(e.orig)
                return {"errors" : error_msg}

            return doctor.to_dict(), 201
        else:
            # Add patient
            try:
                patient = Patient(
                name=json['name'], username=json['username'], email=json['email'], address=json['address'], gender= json['gender'])
                patient.password_hash = json['password']
                db.session.add(patient)
                db.session.commit()
                # Add session
                session['user_id'] = patient.id
            except IntegrityError as e:
                error_msg = str(e.orig)
                return {"errors" : error_msg}

            return patient.to_dict(), 201         
class Login(Resource):

    def post(self):
        # Authenticate user
        pass
class Logout(Resource):
    
    def delete(self):
        session['user_id'] = None
        return {"message" : "204 - No content"}, 204

# Establish Routes

class Home(Resource):

    def get(self):
        return {"message" : "Welcome to Digress API"}, 200
    
class Doctors(Resource):
    def get(self):
        doctors = [doctor.to_dict() for doctor in Doctor.query.all()]
        return jsonify(doctors), 200
    
class DoctorByID(Resource):
    def get(self, id):
        doctor = doctor.query.filter_by(id=id).first().to_dict()
        response = make_response(doctor, 200)
        return response




api.add_resource(Doctors, '/doctors')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Home, '/')





if __name__ == '__main__':
    app.run(port=5555, debug=True)

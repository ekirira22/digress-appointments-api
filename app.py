#!/usr/bin/env python3
from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api
from models.dbmodel import Doctor, Patient, Appointment, Specialization


# Routes
class CheckSession(Resource):
    def get(self):
        user = session.get('username')
        print(user)
        # check if a user is a doctor ot patient
        try:
            doctor = Doctor.query.filter(Doctor.username == user).first()
            patient = Patient.query.filter(Patient.username == user).first()
            if doctor:
                return doctor.to_dict(rules=('-_password_hash',)), 200
            elif patient:
                return patient.to_dict(rules=('-_password_hash',)), 200
        except Exception as e:
            return {"errors": ["invalid request"]}, 401
# Sign a user up
class Signup(Resource):

    def post(self):
        # A user is either a doctor or a patient
        json = request.get_json()

        if json['password'] != json['confirm_password']:
            return {"errors" : ["Passwords do not match"]}, 401
        
        # check if username is unique to both doctors and patients. Get all username
        usernames = [doc.username for doc in Doctor.query.all()]
        usernames.extend([patient.username for patient in Patient.query.all()])

        if json['username'] in usernames:
            return {"errors" : ["username already exists, try another one"]}, 401
        
        if json.get('doctors_id'):
            # Add doctor
            try:
                doctor = Doctor(
                name=json['name'], username=json['username'], email=json['email'], address=json['address'], gender= json['gender'], doctors_id=json['doctors_id'], specialization=json['specialization'])
                doctor.password_hash = json['password']
                db.session.add(doctor)
                db.session.commit()
                # Add session
                session['username'] = doctor.username
            except IntegrityError as e:
                error_msg = str(e.orig)
                return {"errors" : [error_msg]}

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
                session['username'] = patient.username
            except IntegrityError as e:
                error_msg = str(e.orig)
                return {"errors" : error_msg}

            return patient.to_dict(), 201         
class Login(Resource):

    def post(self):
        json = request.get_json()
        try:
            doctor = Doctor.query.filter(Doctor.username == json['username']).first()
            patient = Patient.query.filter(Patient.username == json['username']).first()
            if doctor:
                # Authenticate user. Check password
                if not Doctor.authenticate(doctor, json['password']):
                    return {"errors" : ["Wrong username or password"]}, 401
                session['username'] = doctor.username
                return doctor.to_dict(rules=('-_password_hash',)), 200
            elif patient:
                # Authenticate user. Check password
                if not Patient.authenticate(patient, json['password']):
                    return {"errors" : ["Wrong username or password"]}, 401
                session['username'] = patient.username
                return patient.to_dict(rules=('-_password_hash',)), 200
        except Exception as e:
            return {"errors" : [f"{e} : User does not exist"]}, 401

class Logout(Resource):
    
    def delete(self):
        session['username'] = None
        return {"message" : "204 - No content"}, 204

# Establish Routes

class Home(Resource):

    def get(self):
        return {"message" : "Welcome to Digress API"}, 200
    
class Doctors(Resource):
    def get(self):
        doctors = [doctor.to_dict() for doctor in Doctor.query.all()]
        return doctors, 200
    
class DoctorByID(Resource):
    def get(self, id):
        doctor = Doctor.query.filter_by(id=id).first().to_dict(rules=('-_password_hash',))
        return doctor, 200
    
class Patients(Resource):
    def get(self):
        patients = [patient.to_dict() for patient in Patient.query.all()]
        return patients, 200
    
class PatientById(Resource):
    def get(self, id):
        patient = Patient.query.filter_by(id=id).first().to_dict(rules=('-_password_hash',))
        return patient, 200
    
class Specializations(Resource):
    def get(self):
        specs = [spec.to_dict() for spec in Specialization.query.all()]
        return specs, 200
class  DoctorsBySpecialization(Resource):
    def get(self,specialization):
        doctor=Doctor.query.filter_by(specialization=specialization).first()
        if doctor:
            doctor_dict= doctor.to_dict(rules=("-_password_hash",))
            return make_response(doctor_dict,200)
        else:
            return jsonify({"Message":"Doctor not found"})
api.add_resource(CheckSession, '/check_session')        
api.add_resource(Specializations, '/specializations')
api.add_resource(PatientById, '/patients/<int:id>')
api.add_resource(Patients, '/patients')
api.add_resource(DoctorByID, '/doctors/<int:id>')
api.add_resource(Doctors, '/doctors')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Home, '/')





if __name__ == '__main__':
    app.run(port=5555, debug=True)

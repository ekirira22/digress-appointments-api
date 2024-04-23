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
                    return {"errors" : ["Wrong username or password. Try again"]}, 401
                session['username'] = doctor.username
                return doctor.to_dict(rules=('-_password_hash',)), 200
            elif patient:
                # Authenticate user. Check password
                if not Patient.authenticate(patient, json['password']):
                    return {"errors" : ["Wrong username or password. Try again"]}, 401
                session['username'] = patient.username
                return patient.to_dict(rules=('-_password_hash',)), 200
            else:
                return {"errors" : ["Wrong username or password"]}, 404
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
        doctors = [doctor.to_dict(rules=('-_password_hash',)) for doctor in Doctor.query.all()]
        return doctors, 200
    
    def post(self):
        data = request.get_json()
        try:
            new_doctor = Doctor(
                name = data ['name'],
                username = data ['username'],
                doctors_id = data['doctors_id'],
                email = data ['email'],
                address = data ['address'],
                gender = data ['gender'],
                specialization = data ['specialization'],
                pulse_rate = data ['pulse_rate'],
                blood_pressure = data ['blood_pressure'],
                temparature = data ['temparature'],
                blood_group = data ['blood_group']

            )
            db.session.add(new_doctor)
            db.session.commit()

        except IntegrityError as e:
                error_msg = str(e.orig)
                return {"errors" : error_msg}

    
class DoctorByUserName(Resource):
    def get(self, username):
        doctor = Doctor.query.filter(Doctor.username == username).first().to_dict(rules=('-_password_hash','-appointments'))
        if not doctor:
            return {'error': 'Doctor not found'}, 404
        else:
            doctor.to_dict(rules=('-_password_hash','-appointments')), 200
    
    def patch(self, username):
        doctor = Doctor.query.filter(Doctor.username == username).first()
        if not doctor:
            return {'error': 'Doctor not found'}, 404
        
        data = request.get_json()
        for attr, value in data.items():
            if hasattr(doctor, attr):
                setattr(doctor, attr, value)
            else:
                return {'error': f'Invalid attribute: {attr}'}, 400

        db.session.commit()

        return doctor.to_dict(rules=('-_password_hash',)), 200
        

    def delete(self, username):
        doctor = Doctor.query.filter(Doctor.username == username).first()
        if not doctor:
            return {'error': 'Doctor not found'}, 404
        
        db.session.delete(doctor)
        db.session.commit()
        return '', 204
        
    
class Patients(Resource):
    def get(self):
        patients = [patient.to_dict(rules=('-_password_hash',)) for patient in Patient.query.all()]
        return patients, 200
    def post(self):
        data = request.get_json()
        try:
            new_patient = Patient(
                name = data ['name'],
                username = data ['username'],
                email = data ['email'],
                address = data ['address'],
                gender = data ['gender']
            )
            db.session.add(new_patient)
            db.session.commit()

        except IntegrityError as e:
                error_msg = str(e.orig)
                return {"errors" : error_msg}
    
class PatientByUserName(Resource):
    def get(self, username):
        patient = Patient.query.filter(Patient.username==username).first().to_dict(rules=('-_password_hash',))
        if not patient:
            return {'error': 'Patient not found'}, 404
        else:
            return patient, 200
    
    def patch(self, username):
        patient = Patient.query.filter(Patient.username==username).first()
        if not patient:
            return {'error': 'Patient not found'}, 404
        
        data = request.get_json()
        for attr, value in data.items():
            if hasattr(patient, attr):
                setattr(patient, attr, value)
            else:
                return {'error': f'Invalid attribute: {attr}'}, 400

        db.session.commit()

        response = make_response(
            patient.to_dict(rules=('-_password_hash',)),
            200,
        )
        return response
    def delete(self, username):
        patient = Patient.query.filter(Patient.username==username).first()
        if not patient:
            return {'error': 'Doctor not found'}, 404
        
        db.session.delete(patient)
        db.session.commit()
        return '', 204

    
class Specializations(Resource):
    def get(self):
        specs = [spec.to_dict() for spec in Specialization.query.all()]
        return specs, 200
    
    def patch(self,id):
        pass
    def delete(self, id):
        pass

class DoctorById(Resource):
    def get(self, id):
        doctor = Doctor.query.filter(Doctor.id==id).first().to_dict(rules=('-_password_hash',))
        if not doctor:
            return {'error': ['Doctor not found']}, 404
        else:
            return doctor, 200
        
class PatientById(Resource):
    def get(self, id):
        patient = Patient.query.filter(Patient.id==id).first().to_dict(rules=('-_password_hash',))
        if not patient:
            return {'error': ['Patient not found']}, 404
        else:
            return patient, 200
        
class Appointments(Resource):
    def get(self):
        appointments = [appointment.to_dict() for appointment in Appointment.query.all()]
        return appointments, 200

    def post(self):
        data = request.get_json()
        try:
            new_appointment = Appointment(
                day = data ['day'],
                time = data ['time'],
                doctor_id = data ['doctor_id'],
                patient_id = data ['patient_id'],
            )
            db.session.add(new_appointment)
            db.session.commit()

        except IntegrityError as e:
                error_msg = str(e.orig)
                return {"errors" : error_msg}
        
    def delete(self, id):
        app = Appointment.query.filter(Appointment.id == id).first()
        if app:
            db.session.delete(app)
            db.session.commit()
            response = make_response({}, 204)
        else:
            response = make_response({"error": ["Appointment not found"]}, 404)

        return response

        

api.add_resource(CheckSession, '/check_session')        
api.add_resource(Specializations, '/specializations')
api.add_resource(Appointments, '/appointments')
api.add_resource(PatientByUserName, '/patients/<string:username>')
api.add_resource(PatientById, '/patients/<int:id>')
api.add_resource(Patients, '/patients')
api.add_resource(DoctorByUserName, '/doctors/<string:username>')
api.add_resource(DoctorById, '/doctors/<int:id>')
api.add_resource(Doctors, '/doctors')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Home, '/')





if __name__ == '__main__':
    app.run(port=5555, debug=True)

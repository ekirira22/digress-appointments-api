from random import choice as rc, randrange
from faker import Faker
from app import app
from models.dbmodel import db, Doctor, Patient, Appointment, Specialization
import datetime

fake = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Doctor.query.delete()
        Patient.query.delete()
        Appointment.query.delete()
        Specialization.query.delete()

        print("Seeding specializations...")
        specializations = [
            Specialization(name='Allergy and Immunology'),
            Specialization(name='Anesthesiology'),
            Specialization(name='Cardiology'),
            Specialization(name='Colon and Rectal Surgery'),
            Specialization(name='Emergency Medicine'),
            Specialization(name='Family Medicine'),
            Specialization(name='General Surgery'),
            Specialization(name='Genetics and Genomics'),
            Specialization(name='Neurology'),
            Specialization(name='Obstetrics and Gynecology'),
            Specialization(name='Ophthalmic Surgery'),
            Specialization(name='Orthopaedic Surgery'),
            Specialization(name='Otolaryngology'),
            Specialization(name='Pathology'),
            Specialization(name='Pediatrics'),
            Specialization(name='Physical Medicine and Rehabilitation'),
            Specialization(name='Plastic Surgery'),
            Specialization(name='Psychiatry'),
            Specialization(name='Radiology'),
            Specialization(name='Rheumatology'),
            Specialization(name='Urology'),
            Specialization(name='Vascular Surgery')
        ]
        db.session.add_all(specializations)


        print("Seeding doctors...")
        doctors = []
        doctor_usernames = []
        genders = ['M', 'F', 'O']
        for i in range(100):
            username=fake.first_name() 
            while username not in doctor_usernames:
                i -= 1
                doctor = Doctor(name=fake.name(), username=username, doctors_id=randrange(1000,15000), email=fake.email(), address=fake.address(), gender= rc(genders), specialization=rc(specializations).name)
                doctor.password_hash = "123456"
                doctor_usernames.append(username)
                doctors.append(doctor)

        db.session.add_all(doctors)

        print("Seeding patients...")
        patients = []
        patient_usernames = []
        genders = ['M', 'F', 'O']
        for i in range(100):
            username=fake.first_name()
            while username not in patient_usernames:
                i -= 1
                patient = Patient(name=fake.name(), username=username, email=fake.email(), address=fake.address(), gender= rc(genders))
                patient.password_hash = "123456"
                patient_usernames.append(username)
                patients.append(patient)

        db.session.add_all(patients)

        print("Seeding appointments")
        appointments = []
        for patient in patients:
            doctor = rc(doctors)
            random_date = fake.date()
            random_time = fake.time()
            appointments.append(
                Appointment(patient=patient, doctor=doctor, speciality=doctor.specialization, day=random_date, time=random_time, patient_note=fake.text())
            )
        db.session.add_all(appointments)
        db.session.commit()

        print("Done seeding!")

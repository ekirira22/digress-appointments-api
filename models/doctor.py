from models.dbmodel import db, SerializerMixin, validates, association_proxy
from models.appointment import Appointment

class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    doctors_id = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    address = db.Column(db.String)
    gender = db.Column(db.String)
    specialization = db.Column(db.String)

    # Add relationship
    appointments = db.relationship('Appointment', backref='doctor', cascade='all, delete-orphan')
    patients = association_proxy('appointments', 'patient', creator=lambda patient_obj : Appointment(patient = patient_obj))
    
    # Add serialization
    serialize_rules = ('-appointments.doctor', '-appointments.patient',)

    
    def __repr__(self):
        return f'<Doctor {self.id}>'


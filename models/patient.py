from models.dbmodel import db, SerializerMixin, validates, association_proxy
from models.appointment import Appointment

class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String)
    address = db.Column(db.String)
    gender = db.Column(db.String)

    # Add relationship
    appointments = db.relationship('Appointment', backref='patient', cascade='all, delete-orphan')
    doctors = association_proxy('appointments', 'doctor', creator=lambda doctor_obj : Appointment(doctor = doctor_obj))
    
    # Add serialization
    serialize_rules = ('-vendor_sweets.sweet', '-vendor_sweets.vendor')
    
    def __repr__(self):
        return f'<Patient {self.id}>'

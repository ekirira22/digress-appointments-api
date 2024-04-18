from models.dbmodel import db, SerializerMixin, validates, association_proxy, bcrypt
from models.appointment import Appointment
from sqlalchemy.ext.hybrid import hybrid_property

class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String)
    address = db.Column(db.String)
    gender = db.Column(db.String)

    # Add relationship
    appointments = db.relationship('Appointment', backref='patient', cascade='all, delete-orphan')
    doctors = association_proxy('appointments', 'doctor', creator=lambda doctor_obj : Appointment(doctor = doctor_obj))
    
    # Add serialization
    serialize_rules = ('-appointments.doctor', '-appointments.patient',)

    # password encryption
    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
    def __repr__(self):
        return f'<Patient {self.id}>'

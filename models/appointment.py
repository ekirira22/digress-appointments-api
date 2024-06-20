from models.dbmodel import db, SerializerMixin, validates, association_proxy

class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=True)
    time = db.Column(db.String, nullable=True)
    speciality = db.Column(db.String, nullable=True)
    patient_note = db.Column(db.String, nullable=True)
    # Add relationships
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'))
    # Add serialization
    
    # Add validation
    

    
    def __repr__(self):
        return f'<Appointment {self.id}>'

from models.dbmodel import db, SerializerMixin, validates, association_proxy

class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String)
    time = db.Column(db.String)
    # Add relationships
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    # Add serialization
    
    # Add validation
    

    
    def __repr__(self):
        return f'<Appointment {self.id}>'

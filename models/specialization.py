from models.dbmodel import db, SerializerMixin, validates, association_proxy

class Specialization(db.Model, SerializerMixin):
    __tablename__ = 'specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)    

    
    def __repr__(self):
        return f'<Specialization: {self.id} | {self.name}>'
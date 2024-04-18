from config import db, bcrypt
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


# Models

from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.specialization import Specialization


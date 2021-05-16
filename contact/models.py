from sqlalchemy import Column , Integer, String
from .database import Base

class Contact(Base):
    __tablename__="contact"
    id= Column(Integer, primary_key=True, index=True)
    email= Column(String, unique=True, index=True)
    name= Column(String, index=True)
    mobile_no=Column(Integer)
    

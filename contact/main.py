from typing import Optional

from sqlalchemy.orm import Session, query
from sqlalchemy.sql.sqltypes import Date
from fastapi import FastAPI , Depends, status, HTTPException
from contact.database import Base, SessionLocal, engine
from pydantic import BaseModel
from contact import models
from fastapi.encoders import jsonable_encoder

models.Base.metadata.create_all(engine)


app=FastAPI()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    


class Contact(BaseModel):
    email:str
    name:str
    mobile_no:int


@app.post("/contact", status_code=status.HTTP_201_CREATED)
def create_contact(request: Contact, db:Session = Depends(get_db)):
    new_contact = models.Contact(email = request.email, mobile_no= request.mobile_no, name= request.name)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@app.get("/contacts", status_code=status.HTTP_200_OK)
def fetch_all_contact(db:Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts

@app.get("/contact/{id}", status_code=status.HTTP_200_OK)
def fetch_contact(id: int, db:Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id==id).first()
    return contact

@app.delete("/contact/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(id: int, db:Session = Depends(get_db)):
    db.query(models.Contact).filter(models.Contact.id==id).delete(synchronize_session=False)
    db.commit()
    return {"Contact Deleted successfully"}


@app.put("/contact/{id}", status_code=200)
def update_contact(request: Contact , id: int, db:Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(
        models.Contact.id==id)
    if not contact.first():
        raise HTTPException(status_code=404, detail=f'Contact with ID {id} not found')
    else:
        data = jsonable_encoder(request)
        contact.update(data)
        db.commit()        
        return {"msg":'Contact Updated successfully'}

@app.get("/contact/search/")
def search(search:str, skip: int = 0, limit: int = 10 , db:Session = Depends(get_db)):
    query="SELECT * FROM Contact where email like '%"+search+"%'"
    contact = db.execute(query)
    return contact[skip + limit]

    

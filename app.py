from fastapi import FastAPI, HTTPException, status, Depends
from db_config import get_db
import consultant
from consultant import Consultant
from consultant_schema import Consultant_create, Consultant_info
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List
from db_config import engine
import json

import redis

app = FastAPI()

r = redis.Redis(host='localhost', port=6379, db=0, password=None, socket_timeout=None)

#consultant.Base.metadata.create_all(bind=engine)

@app.get("/consultants", response_model=List[Consultant_info])
def get_consultants(db: Session = Depends(get_db)):
    list_consultant = []
    # Retrieve cached data #####
    cached_consultants = r.hgetall('consultants')
    if cached_consultants:
        for consultant in cached_consultants:
            c = json.loads(cached_consultants[consultant])
            consultant_info = Consultant_info(
                        id=c['id'],
                        name=c['name'],
                        lastName=c['lastName'],
                        legajo=c['legajo'],
                        startDate=c['startDate'],
                        endDate=c['endDate'],
                        seniority=c['seniority'],
                        billable=c['billable'],
                        availability=c['availability'],
                        englishLevel=c['englishLevel'])
            list_consultant.append(consultant_info)
        return list_consultant
    ############################
    for consultant in db.query(Consultant).all():
        consultant_info = Consultant_info(
                        id=consultant.id,
                        name=consultant.Name,
                        lastName=consultant.LastName,
                        legajo=consultant.Legajo,
                        startDate=consultant.StartDate,
                        endDate=consultant.EndDate,
                        seniority=consultant.Seniority,
                        billable=consultant.Billable,
                        availability=consultant.Availability,
                        englishLevel=consultant.EnglishLevel)
        list_consultant.append(consultant_info)
        # Store in cache
        dict_consultant = vars(consultant_info)
        r.hset('consultants', consultant_info.id, json.dumps(dict_consultant))
    return list_consultant

@app.get("/consultants/{consultant_id}", response_model=Consultant_info)
def get_consultant_by_id(db: Session = Depends(get_db), consultant_id=str):
    cached_consultant = r.hget('consultants', consultant_id)
    ##############################
    if cached_consultant:
        consultant = json.loads(cached_consultant)
        consultant_info = Consultant_info(
                        id=consultant['id'],
                        name=consultant['name'],
                        lastName=consultant['lastName'],
                        legajo=consultant['legajo'],
                        startDate=consultant['startDate'],
                        endDate=consultant['endDate'],
                        seniority=consultant['seniority'],
                        billable=consultant['billable'],
                        availability=consultant['availability'],
                        englishLevel=consultant['englishLevel'])
        return consultant_info
    #############################
    consultant = db.query(Consultant).filter(Consultant.id == consultant_id)\
        .filter(Consultant.DeletedDate.is_(None)).first()
    if consultant is not None:
        consultant_info = Consultant_info(
                        id=consultant.id,
                        name=consultant.Name,
                        lastName=consultant.LastName,
                        legajo=consultant.Legajo,
                        startDate=consultant.StartDate,
                        endDate=consultant.EndDate,
                        seniority=consultant.Seniority,
                        billable=consultant.Billable,
                        availability=consultant.Availability,
                        englishLevel=consultant.EnglishLevel)
        # 
        dict_consultant = vars(consultant_info)
        r.hset('consultants', consultant_info.id, json.dumps(dict_consultant))
        return consultant_info
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Consultant does not exist")

@app.post("/consultants")
def create_consultant(consultant_data: Consultant_create,
                      db: Session = Depends(get_db)):
    consultant_id = str(uuid4())
    new_consultant = Consultant(
        id=consultant_id,
        Name=consultant_data.name,
        LastName=consultant_data.lastName,
        Legajo=consultant_data.legajo,
        StartDate=consultant_data.startDate,
        EndDate=consultant_data.endDate,
        Seniority=consultant_data.seniority,
        Billable=consultant_data.billable,                                                             
        Availability=consultant_data.availability,
        EnglishLevel=consultant_data.englishLevel)
    db.add(new_consultant)
    db.commit()
    dict_consultant = vars(consultant_data)
    r.hset('consultants',consultant_id,json.dumps(dict_consultant))
    return consultant_id


@app.put("/consultants/{consultant_id}")
def update_consultant(consultant_data: Consultant_create, db: Session = Depends(get_db),
                      consultant_id=str):
    try:
        consultant = db.query(Consultant).filter(Consultant.id == consultant_id).\
            update({
                    "Name": consultant_data.name,
                    "LastName": consultant_data.lastName,
                    "Legajo": consultant_data.legajo,
                    "StartDate": consultant_data.startDate,
                    "EndDate": consultant_data.endDate,
                    "Seniority": consultant_data.seniority,
                    "Billable": consultant_data.billable,
                    "Availability": consultant_data.availability,
                    "EnglishLevel": consultant_data.englishLevel,
            })
        db.commit()
        # 
        dict_consultant = vars(consultant_data)
        r.hset('consultants',consultant_id,json.dumps(dict_consultant))
        return {"msg": "Consultant has been Update"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error: {e}")

@app.delete("/consultants/{consultant_id}")
def delete_consultant(db: Session = Depends(get_db), consultant_id=str):
    try:
        consultant = db.query(Consultant).filter(
                        Consultant.id == consultant_id).delete()
        db.commit()
        r.hdel('consultants', consultant_id)
        return {"msg": "Consultant has been Delete"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error: {e}")
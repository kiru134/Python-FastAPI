from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import UserBase, UserDisplay
from db.database import get_db
from db import db_user
from auth.oauth2 import get_current_user


router = APIRouter(prefix='/user',
                   tags=['user']
                   )


@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


@router.get('/allusers', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db), current_usr: UserBase = Depends(get_current_user)):
    return db_user.get_all_users(db)


@router.get('/{id}', response_model=UserDisplay)
def get_user_byid(id: int, db: Session = Depends(get_db), current_usr: UserBase = Depends(get_current_user)):
    return db_user.get_user(db, id)


@router.post('/update/{id}')
def update_user_byid(request: UserBase, id: int, db: Session = Depends(get_db), current_usr: UserBase = Depends(get_current_user)):
    return db_user.update_user(db, id, request)


@router.post('/delete/{id}')
def delete_user(id: int, db: Session = Depends(get_db), current_usr: UserBase = Depends(get_current_user)):
    return db_user.delete_user(id, db)

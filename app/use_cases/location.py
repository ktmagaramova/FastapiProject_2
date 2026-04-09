from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.models import Post, User, Category, Location, Comment
from app.schemas import (
    PostCreate, PostRead, PostUpdate,
    UserCreate, UserRead,
    CategoryCreate, CategoryRead,
    LocationCreate, LocationRead,
    CommentCreate, CommentRead
)
from app.database import database
from datetime import datetime

router = APIRouter()
router = APIRouter(prefix="/location", tags=["Location"])
#локация
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=LocationRead)
def create_location(l: LocationCreate) -> LocationRead:
    with database.session() as db:
        db_location = Location(
            name=l.name,
            is_published=True,
            created_at=datetime.utcnow()
        )
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        return LocationRead.model_validate(db_location)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[LocationRead])
async def get_locations(skip: int = 0, limit: int = 100) -> list[LocationRead]:
    with database.session() as db:
        locations = db.query(Location).offset(skip).limit(limit).all()
        return [LocationRead.model_validate(l) for l in locations]


@router.get("/{location_id}", status_code=status.HTTP_200_OK, response_model=LocationRead)
async def get_location(location_id: int) -> LocationRead:
    with database.session() as db:
        location = db.query(Location).filter(Location.id == location_id).first()
        return LocationRead.model_validate(location)


@router.put("/{location_id}", status_code=status.HTTP_200_OK, response_model=LocationRead)
async def update_location(location_id: int, location_data: LocationCreate) -> LocationRead:
    with database.session() as db:
        db_location = db.query(Location).filter(Location.id == location_id).first()
        db_location.name = location_data.name
        db.commit()
        db.refresh(db_location)
        return LocationRead.model_validate(db_location)


@router.delete("/{location_id}", status_code=status.HTTP_200_OK)
async def delete_location(location_id: int) -> dict:
    with database.session() as db:
        db_location = db.query(Location).filter(Location.id == location_id).first()
        db.delete(db_location)
        db.commit()
        return {"detail": "Локация удалена"}


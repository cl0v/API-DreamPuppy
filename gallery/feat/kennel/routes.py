from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from gallery.database import get_db
from . import schemas, crud
from gallery.security import ignore_non_admins

router = APIRouter()


@router.post(
    "/kennels/new",
    response_model=schemas.OutputKennel,
    dependencies=[Depends(ignore_non_admins)],
)
async def add_kennel(kennel: schemas.CreateKennel, db: Session = Depends(get_db)):
    return crud.add_kennel(db, kennel)

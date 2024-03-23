from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from gallery_api_impl.database import get_db
from . import schemas, crud
from gallery_api_impl.security import ignore_non_admins
from gallery_api_impl.feat.puppy import crud as puppy_crud
from gallery_api_impl.feat.puppy.schemas import OutPuppy

router = APIRouter()


# App Gallery:
@router.get(
    "/kennels/{kennel_id}",
    response_model=schemas.OutputKennel,
)
async def get_kennel(kennel_id: int, db: Session = Depends(get_db)):
    return crud.get_kennel(db, kennel_id)


@router.get(
    "/kennels/{kennel_id}/puppies",
    response_model=list[OutPuppy],
    dependencies=[Depends(ignore_non_admins)],
)
def list_puppies_from_kennel(
    kennel_id: int,
    db: Session = Depends(get_db),
):
    ids = crud.list_my_puppies_ids(db, kennel_id)
    tmp = puppy_crud.list_puppies(db, ids)
    return tmp


# App Dashboard:
@router.post(
    "/kennels/new",
    response_model=schemas.OutputKennel,
    dependencies=[Depends(ignore_non_admins)],
)
async def add_kennel(kennel: schemas.CreateKennel, db: Session = Depends(get_db)):
    kennel = crud.add_kennel(db, kennel)
    return kennel

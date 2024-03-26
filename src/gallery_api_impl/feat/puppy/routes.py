from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from gallery_api_impl.database import get_db
from . import schemas, crud
import gallery_api_impl.feat.kennel.crud as kennel_crud
from gallery_api_impl.security import ignore_non_admins

router = APIRouter()


@router.post(
    "/puppies/{puppy_id}/images",
    dependencies=[Depends(ignore_non_admins)],
    description="""
    Adiciona a(s) imagens ao filhote com o respectivo id.
    Retorna o id da imagem na tabela das medias.
    """,
)
def upload_puppy_images(
    puppy_id: int,
    setCover: bool = False,
    db: Session = Depends(get_db),
    **images: list[UploadFile],
):
    return crud.add_puppy_images(db, images, puppy_id=puppy_id, setCover=setCover)


@router.post(
    "/puppies/{puppy_id}/images/coverurl",
    dependencies=[Depends(ignore_non_admins)],
)
def update_cover(
    puppy_id: int,
    # Image id on medias table
    linkTo: int,
    db: Session = Depends(get_db),
):
    # TODO: Implementar sistema de cover
    crud.update_cover_url(db, puppy_id=puppy_id, linkToId=linkTo)
    return "OK"


@router.post(
    "/kennels/{kennel_id}/puppies/new",
    # response_model=schemas.OutputAddPuppy,
    dependencies=[Depends(ignore_non_admins)],
)
def add_puppy(
    kennel_id: int,
    puppy: schemas.PuppyRequestForm,
    db: Session = Depends(get_db),
):
    n_puppy = crud.add_puppy(
        db,
        schema=puppy,
        kennel_id=kennel_id,
    )

    return {
        "id": n_puppy.id,
        "kennel": n_puppy.kennel,
        "status": "OK",
    }


# App Gallery:
@router.patch(
    "/puppies/{puppy_id}",
    response_model=schemas.OutPuppy,
    dependencies=[Depends(ignore_non_admins)],
)
# TODO: Terminar de adicionar endpoint de atualização dos dados do filhote.
def update_puppy(
    puppy_id: int,
    puppy: schemas.InpUpdatePuppyDetails,
    db: Session = Depends(get_db),
):
    puppy = crud.update_puppy(db, puppy, puppy_id)
    return puppy


# App Gallery:
@router.get(
    "/puppies/{puppy_id}",
    response_model=schemas.OutPuppyDetails,
)
def get_puppy(
    puppy_id: int,
    db: Session = Depends(get_db),
):
    puppy = crud.get_puppy(db, puppy_id)
    return puppy


# App Gallery:
@router.get(
    "/puppies/{puppy_id}/kennel",
    response_model=int,
)
def get_kennel_id_from_puppy_id(
    puppy_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_kennel_id_from_puppy_id(db, puppy_id)


# App Dashboard:
@router.post(
    "/breeds/new",
    response_model=schemas.OutputNewBreed,
    dependencies=[Depends(ignore_non_admins)],
)
async def add_breed(breed: schemas.NewBreed, db: Session = Depends(get_db)):
    return crud.add_breed(db, breed)


@router.get(
    "/breeds/list",
    response_model=list[schemas.OutputNewBreed],
)
def list_breeds(db: Session = Depends(get_db)):
    return crud.list_breeds(db)


@router.put(
    "/puppies/{puppy_id}/show",
    dependencies=[Depends(ignore_non_admins)],
)
def show_puppy_on_gallery(
    puppy_id: int,
    db: Session = Depends(get_db),
):
    pid = crud.show_on_gallery(db, puppy_id)
    return {"id": pid, "message": "OK"}


@router.put(
    "/puppies/{puppy_id}/hide",
    dependencies=[Depends(ignore_non_admins)],
)
def hide_puppy_from_gallery(
    puppy_id: int,
    db: Session = Depends(get_db),
):
    pid = crud.hide_from_gallery(db, puppy_id)
    return {"id": pid, "message": "OK"}

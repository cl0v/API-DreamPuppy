from app.database import engine, Base
from fastapi.responses import JSONResponse
from fastapi import Request, FastAPI

from app.feat.gallery.routes import router as gallery_router
from app.feat.puppy.routes import router as puppy_router
from app.feat.kennel.routes import router as kennel_router
from app.feat.gallery.exceptions import GalleryException
from app.feat.puppy.exceptions import PuppyDetailsException, PuppyStorageException
from app.feat.kennel.exceptions import KennelException
from app.env import TEST_NAME


Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

app.include_router(gallery_router)
app.include_router(puppy_router)
app.include_router(kennel_router)


@app.get("/")
def root():
    name = TEST_NAME
    return f"Hello {name} ."


@app.exception_handler(GalleryException)
async def gallery_exception_handler(request: Request, exc: GalleryException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": exc.message,
        },
    )


@app.exception_handler(PuppyDetailsException)
async def puppy_exception_handler(request: Request, exc: PuppyDetailsException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": exc.message,
        },
    )


@app.exception_handler(KennelException)
async def kennel_exception_handler(request: Request, exc: KennelException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": exc.message,
        },
    )


@app.exception_handler(PuppyStorageException)
async def azure_exception_handler(request: Request, exc: PuppyStorageException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": exc.message,
        },
    )

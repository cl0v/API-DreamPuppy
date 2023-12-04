from gallery.database import engine, Base
from fastapi.responses import JSONResponse
from fastapi import Request, FastAPI

from gallery.feat.gallery.routes import router as gallery_router
from gallery.feat.puppy.routes import router as puppy_router
from gallery.feat.kennel.routes import router as kennel_router
from gallery.feat.gallery.exceptions import GalleryException
from gallery.feat.puppy.exceptions import PuppyDetailsException, PuppyStorageException
from gallery.feat.kennel.exceptions import KennelException

Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

app.include_router(gallery_router)
app.include_router(puppy_router)
app.include_router(kennel_router)


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


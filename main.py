import uvicorn
from gallery.database import engine, Base
from fastapi.responses import JSONResponse
from fastapi import Request, FastAPI

from gallery.src.feat.gallery.routes import router as gallery_router
from gallery.src.feat.puppy.routes import router as puppy_router
from gallery.src.feat.gallery.exceptions import GalleryException
from gallery.src.feat.puppy.exceptions import PuppyDetailsException

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(gallery_router)
app.include_router(puppy_router)


@app.exception_handler(GalleryException)
async def gallery_exception_handler(request: Request, exc: GalleryException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": exc.message,
        },
    )


@app.exception_handler(PuppyDetailsException)
async def puppy_details_exception_handler(request: Request, exc: PuppyDetailsException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": exc.message,
        },
    )


# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

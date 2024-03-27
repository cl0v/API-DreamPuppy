from gallery_api_impl.database import engine, Base
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi import Request, FastAPI

from gallery_api_impl.feat.gallery.routes import router as gallery_router
from gallery_api_impl.feat.puppy.routes import router as puppy_router
from gallery_api_impl.feat.kennel.routes import router as kennel_router
from gallery_api_impl.feat.gallery.exceptions import GalleryException
from gallery_api_impl.feat.puppy.exceptions import (
    PuppyException,
    PuppyStorageException,
    MediaException,
)
from gallery_api_impl.feat.kennel.exceptions import KennelException
from gallery_api_impl.env import TEST_NAME, API_VERSION
from fastapi_pagination import add_pagination

Base.metadata.create_all(bind=engine)

# TODO: Utilizar esse boolean por enviroment.
# Facilitando os deploys (Mesmo que eu não suba pro git, ainda buildará a imagem com as alterações locais)
# Sujestão: Fazer com que a rotina do docker build seja feita por um CI/CD pode evitar confusão.
app = FastAPI(
    debug=False,
    docs_url=None,  # Disable docs (Swagger UI)
    redoc_url=None,  # Disable redoc
)

app.include_router(gallery_router)
app.include_router(puppy_router)
app.include_router(kennel_router)


@app.get("/")
def root():
    return f"Hello {TEST_NAME} : {API_VERSION}"


@app.get("/policy.pdf", response_class=FileResponse)
def policy_pdf():
    return "gallery_api_impl/assets/policy.pdf"


@app.get("/policy.docx", response_class=FileResponse)
def policy_docx():
    return "gallery_api_impl/assets/policy.docx"


@app.get("/redir")
def redirToDownloads(isAndroid: bool = False):
    url_loja = "https://apps.apple.com/br/app/dreampuppy-galeria-de-filhotes/id6478811369?l=en-GB"
    if isAndroid:
        url_loja = (
            "https://play.google.com/store/apps/details?id=com.dreampuppy.gallery&pli=1"
        )
    html = """
<!DOCTYPE html>  <!-Define o tipo de documento->
<html>
<head>
    <meta charset="utf-8"/> <!-Define o conjunto de caracteres usados no documento->
    <meta http-equiv="refresh" content="0; URL='{URLHERE}'"/> <!-Define o redirecionamento, tempo e URL->
<title>Ver na Loja</title> <!-Define o título do documento na aba do navegador->
</head>
    <body>
    </body>
</html>
"""
    split = html.split("\n")
    split[5] = split[5].replace("{URLHERE}", url_loja)
    dyn_val_html = "\n".join(split)

    return HTMLResponse(content=dyn_val_html)


@app.exception_handler(GalleryException)
async def gallery_exception_handler(request: Request, exc: GalleryException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": exc.message,
        },
    )


@app.exception_handler(PuppyException)
async def puppy_exception_handler(request: Request, exc: PuppyException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": exc.message,
            "id": exc.id,
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


@app.exception_handler(MediaException)
async def media_exception_handler(request: Request, exc: MediaException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": exc.message,
        },
    )


add_pagination(app)

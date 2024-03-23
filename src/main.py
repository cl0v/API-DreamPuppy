import uvicorn

from gallery_api_impl.main import app

# gallery_api_impl.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )

# uvicorn gallery_api_impl.main:app --reload --port=9900
# (PROD) Remover after debug
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9900)

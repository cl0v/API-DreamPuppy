import uvicorn

from app.main import app

# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )

# uvicorn app.main:app --reload --port=9900
# (PROD) Remover after debug
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9900)

from fastapi import FastAPI

app = FastAPI(
    debug=False,
    docs_url=None,
    redoc_url=None,
)


@app.post("/upload")
def add_pet_to_merchant(pet: dict):
    print('Isso sai no log?')
    pass


@app.put("/delete/{id}")
def delete_pet_from_merchant():
    print('Deletar sai no log?')
    pass

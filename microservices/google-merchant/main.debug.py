from main import app
import uvicorn

uvicorn.run(app, port=9901, host="0.0.0.0")
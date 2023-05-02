from fastapi import FastAPI

app = FastAPI(title="webserver")



@app.get("/")
def hello():
    return {
        "message": "hello"
    }




# gunicorn src.portfolio.app.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
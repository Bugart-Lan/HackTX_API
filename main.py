from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/llm_output")
def llm_output():
    return {"isValid": True, "Response": "Example Response"}

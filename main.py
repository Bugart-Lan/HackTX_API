from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import google.generativeai as genai
import os

os.environ["API_KEY"] = "AIzaSyAj7nR_CNt3rlrAVA3crInL5FsUvEGRGJY"
genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Prompt(BaseModel):
    prompt: str


class QuestionPrompt(BaseModel):
    numQuestion: int
    difficulty: str
    topic: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/response")
async def response(prompt: Prompt):
    response = model.generate_content(
        f"Explain the following concept in a simple way {prompt.prompt}"
    )
    return {"isValid": True, "Response": response.text}


@app.post("/questions")
async def questions(prompt: QuestionPrompt):
    questions = []
    for _ in range(prompt.numQuestion):
        response = model.generate_content(
            f"""Generate a quiz question.
            Topic: {prompt.topic}
            Difficulty level: {prompt.difficulty}
            Format:
                Question
                Choices
                Answer
                Hint
                Explanation
            """
        )
        questions.append(response.text)
    return {"questions": questions}

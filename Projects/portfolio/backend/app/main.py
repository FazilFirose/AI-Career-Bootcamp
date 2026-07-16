from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Portfolio API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Welcome to Fazil's Portfolio API 🚀"
    }


@app.get("/about")
def about():
    return {
        "name": "Fazil Firose Ibrahim",
        "title": "AI Developer | Python Programmer",
        "location": "Kerala, India",
        "description": (
            "Computer Science (Data Science) graduate passionate about "
            "Artificial Intelligence, Python development, automation, "
            "and building practical AI applications."
        )
    }
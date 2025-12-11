from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize Fast API
app = FastAPI()

# CORS setup
# Allowed origins
origins = [
    "http://localhost:5173/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


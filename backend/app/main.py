from fastapi import FastAPI, status, Depends
from fastapi.exceptions import HTTPException


app = FastAPI()

# Users (admin & voters), Candidates, Election, Audit logs

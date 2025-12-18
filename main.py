from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI(title="Daily Fitness Tracker")

templates = Jinja2Templates(directory="templates")

class Workout(BaseModel):
    id: int
    name: str
    description: str
    day: date

workouts: List[Workout] = []
current_id = 1


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    today = date.today()
    today_workouts = [w for w in workouts if w.day == today]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "workouts": today_workouts,
            "today": today
        }
    )

@app.post("/add")
def add_workout(
    name: str = Form(...),
    description: str = Form(...)
):
    global current_id

    workouts.append(
        Workout(
            id=current_id,
            name=name,
            description=description,
            day=date.today()
        )
    )
    current_id += 1

    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{workout_id}")
def delete_workout(workout_id: int):
    global workouts
    workouts = [w for w in workouts if w.id != workout_id]
    return RedirectResponse(url="/", status_code=303)

# ======================
# ЗАПУСК
# uvicorn main:app --reload

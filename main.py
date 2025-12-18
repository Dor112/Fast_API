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

class PresetWorkout(BaseModel):
    name: str
    description: str


workouts: List[Workout] = []
current_id = 1

# Заготовленные примеры тренировок
preset_workouts: List[PresetWorkout] = [
    PresetWorkout(
        name="Грудь и трицепс",
        description="Жим лёжа 4x8, жим гантелей 3x10, отжимания 3x15, французский жим 3x10"
    ),
    PresetWorkout(
        name="Спина и бицепс",
        description="Подтягивания 4x6, тяга штанги 4x8, сгибания рук 3x12"
    ),
    PresetWorkout(
        name="Ноги",
        description="Присед 4x8, жим ногами 3x10, выпады 3x12, икры 4x15"
    ),
    PresetWorkout(
        name="Кардио",
        description="Бег 20 минут или велотренажёр 30 минут, пульс 130–150"
    ),
    PresetWorkout(
        name="Функциональная",
        description="Берпи 3x10, планка 3x60с, прыжки 3x20"
    )
]



@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    today = date.today()
    today_workouts = [w for w in workouts if w.day == today]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "workouts": today_workouts,
            "today": today,
            "presets": preset_workouts
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

@app.post("/add_preset")
def add_preset_workout(preset_name: str = Form(...)):
    global current_id

    preset = next((p for p in preset_workouts if p.name == preset_name), None)
    if preset:
        workouts.append(
            Workout(
                id=current_id,
                name=preset.name,
                description=preset.description,
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

# ЗАПУСК
# uvicorn main:app --reload

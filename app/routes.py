from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .database import SessionLocal, User
from .updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@router.post("/generate-workout")
def generate_workout(
    request: Request,
    name: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    workout_plan = generate_workout_gemini(
        age, weight, goal, intensity
    )

    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    db = SessionLocal()

    user = User(
        name=name,
        user_id=user_id,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
        workout_plan=workout_plan
    )

    db.add(user)
    db.commit()
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip
        }
    )
@router.post("/submit-feedback")
def submit_feedback(
    request: Request,
    feedback: str = Form(...)
):
    updated_plan = update_workout_plan(
        "Previous workout plan",
        feedback
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "workout_plan": updated_plan,
            "nutrition_tip": "Updated based on your feedback."
        }
    )


@router.get("/view-all-users")
def view_all_users(request: Request):
    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users
        }
    )
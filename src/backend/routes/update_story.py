from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from src.backend.database import engine
from src.backend.database.orm import Story
from src.backend.dependencies import cookie
from src.backend.internals.stories import StoryResponse, check_description

app = APIRouter()


def validate_story_exists(story_id):
    with Session(engine) as transaction:
        if Story.get_by_id(transaction, story_id) is not None:
            return True
        return False


@app.patch('/story', response_model=StoryResponse, dependencies=[Depends(cookie)], status_code=201)
def update_story(story_id: int, description: str):
    if validate_story_exists(story_id):
        with Session(engine) as session:
            story = Story.get_by_id(session, story_id)
            if check_description(description):
                story.summary = description
                session.add(story)
                session.commit()
                session.refresh(story)
            else:
                raise HTTPException(status_code=400, detail='Описание истории превышает возможное количество символов')
    else:
        raise HTTPException(status_code=400, detail='История не найдена')
    return story
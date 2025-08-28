from .. import models, schemas, oauth2
from fastapi import FastAPI , Response, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

#@router.get("/", response_model=list[schemas.Post])
@router.get("/", response_model=list[schemas.PostOut])
def get_posts(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db), 
              search: Optional[str] = "", limit: int = 10, skip: int = 0):
    # cursor.execute("""SElECT * FROM posts""")
    # posts = cursor.fetchall()
    
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()



    return results

@router.post("/", response_model=schemas.Post, )
def create_posts(post: schemas.PostCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))

    # post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id {id} was not found"}

    return post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
                   
    # deleted_post = cursor.fetchone()


    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post_query.first() is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id {id} was not found"}

    # conn.commit()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized to perform requested action")


    post_query.delete(synchronize_session=False)
    db.commit()

    response.status_code = status.HTTP_204_NO_CONTENT
    return

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, response: Response, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published,id,))

    # updated_post = cursor.fetchone()

    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id {id} was not found"}

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized to perform requested action")


    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
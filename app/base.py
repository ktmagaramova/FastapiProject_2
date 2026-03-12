from fastapi import APIRouter, status, HTTPException
from app.models import Post

router = APIRouter()
posts: list[Post]=[]#упрощённый список постов

#главная страница с постами
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Post])
async def get_posts() -> list[Post]:
    return posts[::-1]

#посмотреть один конкретный пост
@router.get("/post/{post_id}", status_code=status.HTTP_200_OK, response_model=Post)
async def get_post(post_id: int) -> Post:
   for p in posts:
       if p.id==post_id:
           return p
   raise HTTPException(status_code=404, detail="Пост не найден")

#добавить пост
@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(p: Post) -> Post:
    posts.append(p)
    return p

#изменение поста
@router.put("/post/{post_id}", status_code=status.HTTP_200_OK, response_model=Post)
async def update_post(post_id: int, new_post: Post) -> Post:
   for i, p in enumerate(posts):
       if p.id==post_id:
           posts[i]=new_post
           return posts[i]
   raise HTTPException(status_code=404, detail="Пост не найден")

#удаление поста
@router.delete("/post/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int) -> dict:
   for p in posts:
       if p.id==post_id:
           posts.remove(p)
           return {"text": "Пост удалён"}
   raise HTTPException(status_code=404, detail="Пост не найден")

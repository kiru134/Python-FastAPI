from enum import Enum
from typing import Optional
from fastapi import APIRouter, Depends, status, Response
from routers.blog_post import required_func

router = APIRouter(
    prefix='/blogs',
    tags=['blog']
)


@router.get(
    '/all',
    summary="Retereving all blogs",
    description="this api call simulates fetching all the blogs",
    response_description="This is the list of available blogs"
)
def get_required_Blog(page=1, pagesize: Optional[int] = None, requiredpara: dict = Depends(required_func)):
    return {"message": f'All {page} of size {pagesize}', "req": requiredpara}


@router.get('/{id}/comments/{comment_id}', tags=['comments'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {"message": f'blogid:{id},comment_id:{comment_id},valid:{valid},username:{username}'}


class BlogType(str, Enum):
    short = "short"
    story = "story"


@router.get('/type/{type}')
def get_blog_type(type: BlogType):
    return {"message": "Blog type " + type}


@router.get('/{id}', status_code=status.HTTP_200_OK)
def getBlog(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ("error id not found")
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f'Hello here is your blog id {id}'}

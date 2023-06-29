from typing import Optional, List, Dict
from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel

router = APIRouter(
    prefix='/blogs',
    tags=['blog']
)


class Image(BaseModel):
    url: str
    aials: str


class BlogModel(BaseModel):
    title: str
    nb_comments: int
    published: Optional[str]
    tags: List[str] = []
    metadata: Dict[str, str] = {'key1': 'val1'}
    image: Optional[Image] = None


@router.post('/new/{id}')
def create_Blog(blog: BlogModel, id: int, version: int = 1):
    return {
        "id": id,
        "version": version,
        "data": blog, }


@router.post('new/{id}/comment/{comment_id}')
def create_comment(blog: BlogModel, id: int,
                   comment_title: int = Query(None,
                                              title="Id of the comment",
                                              description="Some desp",
                                              alias='commid',
                                              deprecated=True),
                   content: str = Body(..., min_length=10,
                                       max_length=13,
                                       regex="^[a-z\s]*$"),
                   v: Optional[List[str]] = Query(['1.0', '1.2']),
                   comment_id: int = Path(None, gt=6, le=9)

                   ):
    return {
        "blog": blog,
        'id': id,
        "comment_title": comment_title,
        "content": content,
        "version": v,
        "comm_id": comment_id
    }


def required_func():
    return {"message": "Hi kiru welcome"}

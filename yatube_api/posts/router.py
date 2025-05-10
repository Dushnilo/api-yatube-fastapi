from fastapi import APIRouter, HTTPException, Depends, Query, Request

from config import settings
from posts.models import PostDAO, GroupDAO
from posts.schemas import SPostRequest, SPostResponse, SPostsResponse
from users.auth import validate_access_token
from users.models import User, UsersDAO

router = APIRouter(
    prefix='/api/v1/posts',
    tags=['Publications']
)


async def get_post_or_404(post_id: int, current_user: User):
    post = await PostDAO.find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail='Post not found.')

    user = await UsersDAO.find_one_or_none(email=current_user['sub'])
    if post.author_id != user.id:
        raise HTTPException(
            status_code=403,
            detail='You do not have permission to edit this post.'
        )
    return post


def post_answer(post_data):
    answer = SPostResponse(
        id=post_data.id,
        author=post_data.author.username,
        text=post_data.text,
        pub_date=post_data.pub_date,
        image=post_data.image,
        group=post_data.group_id
    )
    return answer


@router.get(
    '',
    response_model=SPostsResponse,
    summary='Get Publications',
    description=(
        'Retrieve a list of all publications. When using the `limit` '
        'and `offset` parameters, the output should support pagination.'
    )
)
async def read_posts(
        request: Request,
        limit: int = Query(
            default=settings.PAGINATION_DEFAULT_LIMIT,
            ge=settings.PAGINATION_DEFAULT_LIMIT_MIN,
            le=settings.PAGINATION_DEFAULT_LIMIT_MAX
        ),
        offset: int = Query(default=0, ge=0)
):
    posts = await PostDAO.find_all_with_pagination(
        'author', offset=offset, limit=limit)
    answer = [post_answer(post) for post in posts]

    total_count = await PostDAO.get_total_count()

    base_url = str(request.url).split('?')[0]
    next_url = (
        f'{base_url}?offset={offset + limit}&limit={limit}'
        if len(answer) == limit
        else None
    )
    previous_url = (
        f'{base_url}?offset={max(offset - limit, 0)}&limit={limit}'
        if offset > 0
        else None
    )

    return {
        'count': total_count,
        'next': next_url,
        'previous': previous_url,
        'results': answer
    }


@router.post(
    '',
    response_model=SPostResponse,
    summary='Create Publication',
    description=('Add a new publication to the collection of publications. '
                 'Anonymous requests are not allowed.')
)
async def create_post(post_data: SPostRequest,
                      current_user: dict = Depends(validate_access_token)):
    if post_data.group:
        group = await GroupDAO.find_one_or_none(id=post_data.group)
        if not group:
            raise HTTPException(status_code=404, detail='Group not found.')

    user = await UsersDAO.find_one_or_none(email=current_user['sub'])
    if not user:
        raise HTTPException(status_code=404, detail='User error.')

    new_post = await PostDAO.add(
        'author',
        text=post_data.text,
        image=post_data.image,
        group_id=post_data.group,
        author_id=user.id
    )

    return post_answer(new_post)


@router.get(
    '/{post_id}',
    response_model=SPostResponse,
    summary='Get Publication',
    description='Retrieve a publication by its ID.'
)
async def read_post_by_id(post_id: int):
    post = await PostDAO.find_one_or_none('author', id=post_id)
    if post is None:
        raise HTTPException(status_code=404)
    return post_answer(post_data=post)


@router.put(
    '/{post_id}',
    response_model=SPostResponse,
    summary='Update Publication',
    description=(
        'Update a publication by its ID. Only the author of the '
        'publication can update it. Anonymous requests are not allowed.'
    )
)
async def update_post(post_id: int, post_data: SPostRequest,
                      current_user: dict = Depends(validate_access_token)):
    await get_post_or_404(post_id, current_user)

    if post_data.group:
        group = await GroupDAO.find_one_or_none(id=post_data.group)
        if not group:
            raise HTTPException(status_code=404, detail='Group not found.')

    data = {'text': post_data.text}
    if post_data.group:
        data.update({'group_id': post_data.group})
    if post_data.image:
        data.update({'image': post_data.image})

    updated_post = await PostDAO.update(post_id, 'author', **data)

    return post_answer(post_data=updated_post)


@router.delete(
    '/{post_id}',
    summary='Delete Publication',
    description=(
        'Delete a publication by its ID. Only the author of the publication '
        'can delete it. Anonymous requests are not allowed.'
    )
)
async def delete_post(post_id: int,
                      current_user: dict = Depends(validate_access_token)):
    await get_post_or_404(post_id, current_user)
    await PostDAO.delete(model_id=post_id)
# 

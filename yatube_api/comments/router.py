from fastapi import APIRouter, HTTPException, Depends, Body

from comments.schemas import SCommentResponse
from posts.models import PostDAO, CommentDAO
from posts.router import get_post_or_404
from users.auth import validate_access_token
from users.models import UsersDAO

router = APIRouter(
    prefix='/api/v1/posts',
    tags=['Comments']
)


async def get_comment_or_404(post_id: int, id: int, current_user: dict):
    comment = await CommentDAO.find_one_or_none('author',
                                                post_id=post_id, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found.')

    user = await UsersDAO.find_one_or_none(email=current_user['sub'])
    if comment.author_id != user.id:
        raise HTTPException(
            status_code=403,
            detail='You do not have permission to edit this comment.'
        )
    return comment


def comment_answer(comment_data):
    answer = SCommentResponse(
        id=comment_data.id,
        author=comment_data.author.username,
        text=comment_data.text,
        created=comment_data.created,
        post=comment_data.post_id
    )
    return answer


@router.get(
    '/{post_id}/comments',
    response_model=list[SCommentResponse],
    summary='Get Comments',
    description='Retrieve all comments for a publication.'
)
async def read_comments(post_id: int):
    post = await PostDAO.find_one_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail='Post not found.')

    comments = await CommentDAO.find_all('author', post_id=post_id)
    return [comment_answer(comment_data=comment) for comment in comments]


@router.post(
    '/{post_id}/comments',
    response_model=SCommentResponse,
    summary='Add Comment',
    description=('Add a new comment to a publication. Anonymous requests are '
                 'not allowed')
)
async def create_comment(post_id: int, text: str = Body(..., embed=True),
                         current_user: dict = Depends(validate_access_token)):
    await get_post_or_404(post_id, current_user)

    user = await UsersDAO.find_one_or_none(email=current_user['sub'])
    if not user:
        raise HTTPException(status_code=404, detail='User error.')

    new_comment = await CommentDAO.add(
        'author',
        text=text,
        author_id=user.id,
        post_id=post_id
    )
    return comment_answer(comment_data=new_comment)


@router.get(
    '/{post_id}/comments/{id}',
    response_model=SCommentResponse,
    summary='Get Comment',
    description='Retrieve a comment for a publication by its ID.'
)
async def read_comment_by_id(post_id: int, id: int):
    comment = await CommentDAO.find_one_or_none('author',
                                                post_id=post_id, id=id)
    if comment is None:
        raise HTTPException(status_code=404)
    return comment_answer(comment_data=comment)


@router.put(
    '/{post_id}/comments/{id}',
    response_model=SCommentResponse,
    summary='Update Comment',
    description=(
        'Update a comment for a publication by its ID. Only the author of the '
        'comment can update it. Anonymous requests are not allowed.'
    )
)
async def update_comment(
    post_id: int,
    id: int,
    text: str = Body(..., embed=True),
    current_user: dict = Depends(validate_access_token)
):
    await get_comment_or_404(post_id=post_id, id=id, current_user=current_user)
    updated_comment = await CommentDAO.update(id, 'author', text=text)
    return comment_answer(comment_data=updated_comment)


@router.delete(
    '/{post_id}/comments/{id}',
    summary='Delete Comment',
    description=(
        'Delete a comment for a publication by its ID. Only the author of the '
        'comment can delete it. Anonymous requests are not allowed.'
    )
)
async def delete_comment(post_id: int, id: int,
                         current_user: dict = Depends(validate_access_token)):
    await get_comment_or_404(post_id=post_id, id=id, current_user=current_user)
    await CommentDAO.delete(model_id=id)
#

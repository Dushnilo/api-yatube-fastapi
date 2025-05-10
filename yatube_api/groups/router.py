from fastapi import APIRouter, HTTPException

from groups.schemas import SGroupResponse
from posts.models import GroupDAO

router = APIRouter(
    prefix='/api/v1/groups',
    tags=['Groups']
)


@router.get(
    '',
    response_model=list[SGroupResponse],
    summary='List of Communities',
    description='Retrieve a list of available communities.'
)
async def read_groups_all():
    return await GroupDAO.find_all()


@router.get(
    '/{group_id}',
    response_model=SGroupResponse,
    summary='Community Information',
    description='Retrieve information about a community by its ID.'
)
async def read_group_by_id(group_id: int):
    group = await GroupDAO.find_one_or_none(id=group_id)
    if group is None:
        raise HTTPException(status_code=404)
    return group

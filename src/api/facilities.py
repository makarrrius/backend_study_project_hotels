from fastapi import Body, Query, APIRouter

from src.schemas.facilities import FacilitiesAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_facilities(
    db: DBDep
):
    return await db.facilities.get_all()

@router.post("")
async def create_facility(
    db: DBDep,
    facility_data: FacilitiesAdd = Body()
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {'status': 'OK', "data": facility}

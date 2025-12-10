import json

from fastapi import Body, Query, APIRouter

from src.schemas.facilities import FacilitiesAdd
from src.api.dependencies import DBDep
from src.init import redis_manager

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_facilities(
    db: DBDep
):
    facilities_from_cache = await redis_manager.get("facilities")
    print(f'{facilities_from_cache=}')
    if not facilities_from_cache:
        print('в кэше нет фасилитис')
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 10)

        return facilities
    else:
        facilities_from_dict = json.loads(facilities_from_cache)
        print('в кэше есть фасилитис')
        return facilities_from_dict

@router.post("")
async def create_facility(
    db: DBDep,
    facility_data: FacilitiesAdd = Body()
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {'status': 'OK', "data": facility}

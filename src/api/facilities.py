from fastapi_cache.decorator import cache
from fastapi import Body, APIRouter

from src.schemas.facilities import FacilitiesAdd
from src.api.dependencies import DBDep
from src.tasks.tasks import test_task
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("ИДУ В БД")
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilitiesAdd = Body()):
    facility = await FacilityService(db).create_facility(facility_data)
    return {"status": "OK", "data": facility}

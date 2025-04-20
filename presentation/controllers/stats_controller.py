from fastapi import APIRouter, Depends
from application.services.zoo_statistics_service import ZooStatisticsService
from presentation.container import get_stats_service

router = APIRouter(prefix="/stats")

@router.get("/animals")
def get_animal_stats(service: ZooStatisticsService = Depends(get_stats_service)):
    return {"total_animals": service.get_animal_count()}

@router.get("/enclosures/free")
def get_free_enclosures(service: ZooStatisticsService = Depends(get_stats_service)):
    return {"free_enclosures": len(service.get_free_enclosures())}
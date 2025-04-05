# presentation/controllers/enclosure_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from domain.entities.Enclosure import Enclosure
from domain.value_objects.EnclosureType import EnclosureType
from infrastructure.repositories.in_memory_animal_repository import InMemoryAnimalRepository
from infrastructure.repositories.in_memory_enclosure_repository import InMemoryEnclosureRepository
from presentation.container import get_animal_repo, get_enclosure_repo

import uuid

router = APIRouter(prefix="/enclosures")

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_enclosure(
    enclosure_type: str,
    size: float,
    max_capacity: int,
    enclosure_repo: InMemoryEnclosureRepository = Depends(get_enclosure_repo)
):
    try:
        # Валидация типа вольера
        type_vo = EnclosureType(enclosure_type)
        
        # Создание вольера
        # enclosure = Enclosure(
        #     id=str(len(enclosure_repo.get_all()) + 1),
        #     enclosure_type=type_vo,
        #     size=size,
        #     max_capacity=max_capacity
        # )

        enclosure = Enclosure(
            id=None, #str(uuid.uuid4()),  # Уникальный ID
            enclosure_type=type_vo,
            size=size,
            max_capacity=max_capacity
        )

        enclosure_repo.save(enclosure)
        return {"id": enclosure.id, "type": enclosure_type}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_all_enclosures(enclosure_repo: InMemoryEnclosureRepository = Depends(get_enclosure_repo)):
    return enclosure_repo.get_all()

@router.get("/{enclosure_id}")
def get_enclosure(
    enclosure_id: str,
    enclosure_repo: InMemoryEnclosureRepository = Depends(get_enclosure_repo)
):
    enclosure = enclosure_repo.get_by_id(enclosure_id)
    if not enclosure:
        raise HTTPException(status_code=404, detail="Enclosure not found")
    return enclosure

@router.delete("/{enclosure_id}")
def delete_enclosure(
    enclosure_id: str,
    enclosure_repo: InMemoryEnclosureRepository = Depends(get_enclosure_repo)
):
    if not enclosure_repo.get_by_id(enclosure_id):
        raise HTTPException(status_code=404, detail="Enclosure not found")
    enclosure_repo.delete(enclosure_id)
    return {"message": "Enclosure deleted"}

@router.post("/{enclosure_id}/add_animal")
def add_animal_to_enclosure(
    enclosure_id: str,
    animal_id: str,
    enclosure_repo: InMemoryEnclosureRepository = Depends(get_enclosure_repo),
    animal_repo: InMemoryAnimalRepository = Depends(get_animal_repo)
):
    try:
        enclosure = enclosure_repo.get_by_id(enclosure_id)
        animal = animal_repo.get_by_id(animal_id)
        
        if not enclosure or not animal:
            raise HTTPException(status_code=404, detail="Object not found")
        
        enclosure.add_animal(animal)
        enclosure_repo.save(enclosure)
        return {"message": "Animal added to enclosure"}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{enclosure_id}/remove_animal")
def remove_animal_from_enclosure(
    enclosure_id: str,
    animal_id: str,
    enclosure_repo: InMemoryEnclosureRepository = Depends(get_enclosure_repo),
    animal_repo: InMemoryAnimalRepository = Depends(get_animal_repo)
):
    try:
        enclosure = enclosure_repo.get_by_id(enclosure_id)
        animal = animal_repo.get_by_id(animal_id)
        
        if not enclosure or not animal:
            raise HTTPException(status_code=404, detail="Object not found")
        
        enclosure.remove_animal(animal)
        enclosure_repo.save(enclosure)
        return {"message": "Animal removed from enclosure"}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
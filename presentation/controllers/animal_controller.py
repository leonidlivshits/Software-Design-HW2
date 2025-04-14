# # presentation/controllers/animal_controller.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from application.services.animal_transfer_service import AnimalTransferService
# from domain.entities import Animal
# from domain.value_objects import Species


# from infrastructure.repositories.in_memory_animal_repository import InMemoryAnimalRepository
# from presentation.container import Container


# router = APIRouter(prefix="/animals")
# container = Container()

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_animal(
#     species: str,
#     name: str,
#     birth_date: str,
#     gender: str,
#     favorite_food: str,
#     animal_repo: InMemoryAnimalRepository = Depends(Container.animal_repo)
# ):
#     try:
#         species_vo = Species(species)
#         animal = Animal(
#             id=str(len(animal_repo.get_all()) + 1),
#             species=species_vo,
#             name=name,
#             birth_date=birth_date,
#             gender=gender,
#             favorite_food=favorite_food
#         )
#         animal_repo.save(animal)
#         return {"id": animal.id, "name": animal.name}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.get("/")
# def get_all_animals(animal_repo: InMemoryAnimalRepository = Depends(Container.animal_repo)):
#     return animal_repo.get_all()

# @router.get("/{animal_id}")
# def get_animal(animal_id: str, animal_repo: InMemoryAnimalRepository = Depends(Container.animal_repo)):
#     animal = animal_repo.get_by_id(animal_id)
#     if not animal:
#         raise HTTPException(status_code=404, detail="Animal not found")
#     return animal

# @router.delete("/{animal_id}")
# def delete_animal(animal_id: str, animal_repo: InMemoryAnimalRepository = Depends(Container.animal_repo)):
#     if not animal_repo.get_by_id(animal_id):
#         raise HTTPException(status_code=404, detail="Animal not found")
#     animal_repo.delete(animal_id)
#     return {"message": "Animal deleted"}

# @router.post("/{animal_id}/move")
# def move_animal(
#     animal_id: str,
#     new_enclosure_id: str,
#     transfer_service: AnimalTransferService = Depends(Container.animal_transfer_service) 
# ):
#     try:
#         event = transfer_service.move_animal(animal_id, new_enclosure_id)
#         return {"message": "Animal moved", "event": event}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter, Depends, HTTPException, status
from application.services.animal_transfer_service import AnimalTransferService
from domain.entities.Animal import Animal
from domain.value_objects.Species import Species

from infrastructure.repositories.in_memory_animal_repository import InMemoryAnimalRepository
from presentation.container import get_animal_repo, get_transfer_service

router = APIRouter(prefix="/animals")

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_animal(
    species: str,
    name: str,
    birth_date: str,
    gender: str,
    is_healthy: bool = True,
    animal_repo: InMemoryAnimalRepository = Depends(get_animal_repo),

):
    try:
        species_vo = Species(species)
        animal = Animal(
            id=str(len(animal_repo.get_all()) + 1),
            species=species_vo,
            name=name,
            birth_date=birth_date,
            gender=gender,
            is_healthy=is_healthy
        )
        animal_repo.save(animal)
        return {"id": animal.id, "name": animal.name}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def get_all_animals(animal_repo: InMemoryAnimalRepository = Depends(get_animal_repo)):
    return animal_repo.get_all()


@router.get("/{animal_id}")
def get_animal(animal_id: str, animal_repo: InMemoryAnimalRepository = Depends(get_animal_repo)):
    animal = animal_repo.get_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@router.delete("/{animal_id}")
def delete_animal(animal_id: str, animal_repo: InMemoryAnimalRepository = Depends(get_animal_repo)):
    if not animal_repo.get_by_id(animal_id):
        raise HTTPException(status_code=404, detail="Animal not found")
    animal_repo.delete(animal_id)
    return {"message": "Animal deleted"}

@router.post("/{animal_id}/heal")
def heal_animal(
    animal_id: str,
    animal_repo: InMemoryAnimalRepository = Depends(get_animal_repo)
):
    animal = animal_repo.get_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    animal.heal()
    animal_repo.save(animal)
    return {"message": "Animal healed"}

@router.post("/{animal_id}/move")
def move_animal(
    animal_id: str,
    new_enclosure_id: str,
    transfer_service: AnimalTransferService = Depends(get_transfer_service)
):
    try:
        event = transfer_service.move_animal(animal_id, new_enclosure_id)
        return {"message": "Animal moved", "event": event}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

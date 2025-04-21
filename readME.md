# Мини-ДЗ №2 КПО  
# Выполнил Лившиц Леонид Игоревич, группа БПИ‑235

### 1. Про функционал  
В задании требовалось реализовать три основных сущности: **Animal**, **Enclosure**, **FeedingSchedule**, а также соответствующие сервисы и контроллеры для работы с зоопарком.

**Animal** (domain/entities/Animal.py):  
```python
class Animal:
    def __init__(self, id: str, species: Species, name: str,
                 birth_date: str, gender: str, is_healthy: bool = True):
        self.id = id
        self.species = species
        self.name = name
        self.birth_date = birth_date
        self.gender = gender
        self.is_healthy = is_healthy
        self.enclosure_id = None

    def feed(self, food_type: str) -> None:
        if food_type != self.species.food_type:
            raise ValueError("Животное отказывается есть эту пищу")
        if not self.is_healthy:
            raise ValueError("Невозможно кормить больное животное")

    def heal(self) -> None:
        self.is_healthy = True
```

**Enclosure** (domain/entities/Enclosure.py):  
```python
class Enclosure:
    def __init__(self, id: str, enclosure_type: EnclosureType, max_capacity: int):
        self.id = id
        self.type = enclosure_type
        self.max_capacity = max_capacity
        self.current_animals: list[str] = []

    def add_animal(self, animal: Animal) -> None:
        if len(self.current_animals) >= self.max_capacity:
            raise ValueError("Вольер переполнен")
        if animal.species.compatible_enclosure_type != self.type:
            raise ValueError("Несовместимый тип вольера")
        if animal.id in self.current_animals:
            raise ValueError("Животное уже находится в этом вольере")
        self.current_animals.append(animal.id)
        animal.enclosure_id = self.id

    def remove_animal(self, animal: Animal) -> None:
        if animal.id not in self.current_animals:
            raise ValueError("Животное не находится в этом вольере")
        self.current_animals.remove(animal.id)
        animal.enclosure_id = None
```

**FeedingSchedule** (domain/entities/FeedingShedule.py):  
```python
class FeedingSchedule:
    def __init__(self, id: str, animal: Animal,
                 feeding_time: FeedingTime, food_type: str):
        self.id = id
        self.animal = animal
        self.feeding_time = feeding_time
        self.food_type = food_type
        self.is_completed = False

    def mark_as_completed(self):
        self.is_completed = True
```

Для взаимодействия с этими сущностями реализованы сервисы:  
- **AnimalTransferService** — перемещение между вольерами и генерация события перемещения.  
- **FeedingOrganizationService** — создание расписаний кормления и выполнение кормления через события.  
- **ZooStatisticsService** — подсчёт общего числа животных и поиск свободных вольеров.

Контроллеры на FastAPI (presentation/controllers) обёртывают эти сервисы в HTTP‑эндпоинты:  
- `/animals` — CRUD для животных;  
- `/enclosures` — CRUD и операции add/remove animal;  
- `/feeding-schedules` — создание/просмотр/завершение расписаний;  
- `/stats` — статистика по зоопарку.

### 2. Принципы чистой архитектуры  
Проект разделён на четыре слоя:

- **Domain** (`domain/`) — чистые сущности и value‑objects без внешних зависимостей.
- **Application** (`application/`) — сервисы, которые реализуют бизнес‑логику поверх доменных моделей.
- **Infrastructure** (`infrastructure/`) — in‑memory репозитории и реализация интерфейсов хранилищ.
- **Presentation** (`presentation/`) — контроллеры FastAPI и настройка зависимостей.

Слои связаны только через интерфейсы (протоколы):  
- Domain не зависит ни от каких внешних библиотек или слоёв вовне.  
- Application зависит от Domain (моделей и репозиториев).  
- Infrastructure зависит от Domain и реализует интерфейсы репозиториев.  
- Presentation зависит от Application и Infrastructure через DI-контейнер.

### 3. Принципы DDD  

- **Ядро домена (Domain Layer)** инкапсулирует основные правила: проверка совместимости вида и типа вольера, ограничения по кормлению больных животных.
- **Value Objects** (`Species`, `EnclosureType`, `FeedingTime`) в `domain/value_objects` несут неизменяемые правила валидации.
- **События** (`AnimalMovedEvent`, `FeedingTimeEvent`) отражают ключевые бизнес‑события перемещения и кормления.
- **Репозитории** (`IAnimalRepository`, `IEnclosureRepository`, `IFeedingScheduleRepository`) задают контракты для сохранения и поиска агрегатов.
- **Сервисы предметной области** (`AnimalTransferService`, `FeedingOrganizationService`, `ZooStatisticsService`) реализуют операции, координирующие несколько сущностей.

Таким образом, проект следует подходу DDD и поддерживает отделение бизнес‑логики от деталей хранения и доставки API.


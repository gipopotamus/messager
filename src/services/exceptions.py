from typing import Generic, TypeVar

T = TypeVar("T")


class ServiceError(Exception):
    """Базовая ошибка бизнес-логики."""


class NotFoundError(ServiceError, Generic[T]):
    def __init__(self, entity_id: int):
        self.entity_id = entity_id
        try:
            self.entity_type = self.__orig_class__.__args__[0]
            self.entity_name = self.entity_type.__name__
        except (AttributeError, IndexError):
            self.entity_name = "Entity"

        super().__init__(f"{self.entity_name} #{entity_id} not found")


class PermissionDeniedError(ServiceError):
    def __init__(self, entity: str, entity_id: int):
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f"No permission to access {entity} #{entity_id}")

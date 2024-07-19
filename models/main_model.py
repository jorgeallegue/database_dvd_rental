from abc import ABC, abstractmethod

class Director:
    def __init__(self, nombre: str, id: int = -1):
        self.nombre = nombre
        self.id = id

class DAO(ABC):
    """
    @abstractmethod
    def create(self, instancia):
        pass
    
    @abstractmethod
    def update(self, instancia):
        pass
    
    @abstractmethod
    def delete(self, id: int):
        pass
    
    @abstractmethod
    def read(self, id: int):
        pass
    """
    @abstractmethod
    def findAll(self):
        pass
        
class DAO_CSV_Director(DAO):
    
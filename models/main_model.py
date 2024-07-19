from abc import ABC, abstractmethod
import csv

class Director:
    def __init__(self, nombre: str, id: int = -1):
        self.nombre = nombre
        self.id = id
    
    def __repr__(self) -> str:
        return f"Director ({self.id}): {self.nombre}"
    
    def __eq__(self, other:object) -> bool:
        if isinstance(other,Director):
            return self.nombre == other.nombre and self.id == other.id
        return False

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
    def __init__(self, path):
        self.path = path

    def findAll(self):
        with open(self.path, "r", newline="") as fichero:
            lector_csv = csv.DictReader(fichero, delimiter=";", quotechar="´")
            lista = []
            for registro in lector_csv:
                lista.append(Director(registro["nombre"], int(registro["id"])))
        return lista
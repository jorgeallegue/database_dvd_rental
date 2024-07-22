from abc import ABC, abstractmethod
import csv

class Model(ABC):
    @classmethod
    @abstractmethod
    def create_from_dict(cls, diccionario):
        pass

    @classmethod
    @abstractmethod
    def create_dict_from_instance(cls, instancia):
        pass

class Director(Model):
    @classmethod
    def create_from_dict(cls, diccionario):
        return cls(diccionario["nombre"], int(diccionario["id"]))
    
    @classmethod
    def create_dict_from_instance(cls, instancia):
        return {"nombre": instancia.nombre, "id": instancia.id}

    def __init__(self, nombre: str, id: int = -1) -> None:
        self.nombre = nombre
        self.id = id

    def __repr__(self) -> str:
        return f"Director ({self.id}): {self.nombre}"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id and self.nombre == other.nombre
        return False
    
    def __hash__(self) -> int:
        return hash((self.id, self.nombre))

class Pelicula(Model):
    @classmethod
    def create_from_dict(cls, diccionario):
        return cls(diccionario["titulo"], 
                   diccionario["sinopsis"], 
                   int(diccionario["director_id"]), 
                   int(diccionario["id"]))
    
    @classmethod
    def create_dict_from_instance(cls, instancia):
        return {
            "id": instancia.id,
            "titulo": instancia.titulo,
            "sinopsis": instancia.sinopsis,
            "director_id": instancia._id_director
        }
    
    def __init__(self, titulo: str, sinopsis: str, director: object, id = -1):
        self.titulo = titulo
        self.sinopsis = sinopsis
        self.id = id
        self.director = director
                
    @property
    def director(self):
        return self._director
    
    @director.setter
    def director(self, value):
        if isinstance(value, Director):
            self._director = value
            self._id_director = value.id
        elif isinstance(value, int):
            self._director = None
            self._id_director = value
        else:
            raise TypeError(f"{value} debe ser un entero o instancia de Director")

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.titulo == other.titulo and self.sinopsis == other.sinopsis and self.director == other.director and self.id == other.id
        return False
    
    def __hash__(self) -> int:
        return hash((self.id, self.titulo, self.sinopsis, self.director))
    
    def __repr__(self) -> str:
        return f"Pelicula ({self.id}): {self.titulo}, {self.director}"

class Genero(Model):
    @classmethod
    def create_from_dict(cls, diccionario):
        return cls(diccionario["genero"], int(diccionario["id"]))
    
    @classmethod
    def create_dict_from_instance(cls, instancia):
        return {"id": instancia.id, "genero": instancia.genero}

    def __init__(self, genero, id=-1) -> None:
        self.id = id
        self.genero = genero

    def __repr__(self) -> str:
        return f"Genero({self.id}): {self.genero}"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id and self.genero == other.genero
        return False
    
    def __hash__(self) -> int:
        return hash((self.id, self.genero))
    
class Copia(Model):
    @classmethod
    def create_from_dict(cls, diccionario):
        return cls(int(diccionario["id_pelicula"]), int(diccionario["id_copia"]))
    
    @classmethod
    def create_dict_from_instance(cls, instancia):
        return {"id_copia": instancia.id, "id_pelicula": instancia.id_pelicula}
    
    def __init__(self,id_pelicula, id = -1) -> None:
        self.id_pelicula = id_pelicula
        self.id = id
    
    def __repr__(self) -> str:
        return f"Copia ID {self.id}, Pelicula ID {self.id_pelicula}"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.id_pelicula == other.id_pelicula and self.id == other.id
        return False
    
    def __hash__(self) -> int:
        return hash((self.id, self.id_pelicula))

class DAO(ABC):

    @abstractmethod
    def guardar(self, instancia):
        pass
    
    @abstractmethod
    def actualizar(self, instancia):
        pass
    
    @abstractmethod
    def borrar(self, id: int):
        pass
    
    @abstractmethod
    def consultar(self, id: int):
        pass

    @abstractmethod
    def todos(self):
        pass

class DAO_CSV(DAO):
    model = None

    def __init__(self, path, encoding = "utf-8"):
        self.path = path
        self.encoding = encoding

    def todos(self):
        with open(self.path, "r", newline="", encoding = self.encoding) as fichero:
            lector_csv = csv.DictReader(fichero, delimiter=";", quotechar="'")
            lista = []
            for registro in lector_csv:
                lista.append(self.model.create_from_dict(registro))
        return lista

    def guardar(self, instancia):
        diccionario = self.model.create_dict_from_instance(instancia)
        with open(self.path, "a", newline="", encoding = self.encoding) as fichero:
            escribir_csv = csv.DictWriter(fichero, delimiter = ";", quotechar = "'", fieldnames = list(diccionario.keys()), lineterminator='\n')
            escribir_csv.writerow(diccionario)
    
    def consultar(self, id):
        lista_consulta = self.todos()
        for consulta in lista_consulta:
            if consulta.id == id:
                return consulta
        return None
    
    def borrar(self, id):
        consulta = self.consultar(id)
        lista_consulta = self.todos()
        if consulta in lista_consulta:
            lista_consulta.remove(consulta)
        fieldnames = list(self.model.create_dict_from_instance(consulta).keys())
        with open(self.path, "w", newline="", encoding = self.encoding) as fichero:
            escribir_csv = csv.DictWriter(fichero, delimiter=";", quotechar="'", fieldnames=fieldnames, lineterminator='\n')
            escribir_csv.writeheader()
            for registro in lista_consulta:
                escribir_csv.writerow(self.model.create_dict_from_instance(registro))
    
    def actualizar(self, instancia):
        lista_consulta = self.todos()
        for i, registro in enumerate(lista_consulta):
            if registro.id == instancia.id:
                lista_consulta[i] = instancia
        fieldnames = list(self.model.create_dict_from_instance(instancia).keys())
        with open(self.path, "w", newline="", encoding=self.encoding) as fichero:
            escribir_csv = csv.DictWriter(fichero, delimiter=";", quotechar="'", fieldnames=fieldnames, lineterminator='\n')
            escribir_csv.writeheader()
            for registro in lista_consulta:
                escribir_csv.writerow(self.model.create_dict_from_instance(registro))     

class DAO_CSV_Director(DAO_CSV):
    model = Director

class DAO_CSV_Pelicula(DAO_CSV):
    model = Pelicula

class DAO_CSV_Genero(DAO_CSV):
    model = Genero

class DAO_CSV_Copia(DAO_CSV):
    model = Copia
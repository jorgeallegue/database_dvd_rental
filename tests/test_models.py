from models.main_model import Director, DAO_CSV_Director, Pelicula, DAO_CSV_Pelicula, Genero, DAO_CSV_Genero

def test_create_director():
    director = Director("Robert Redford")

    assert director.nombre == "Robert Redford"
    assert director.id == -1

def test_dao_directores_traer_todos():
    dao = DAO_CSV_Director("tests/data/directores.csv")
    directores = dao.todos()

    assert len(directores) == 8
    assert directores[7] == Director("Charlie Chaplin", 8)

def test_create_pelicula():
    pelicula = Pelicula("El señor de los anillos", "Sauron es muy malo", 9)

    assert pelicula.titulo == "El señor de los anillos"
    assert pelicula.sinopsis == "Sauron es muy malo"
    assert pelicula._id_director == 9
    assert pelicula.id == -1
    assert pelicula.director is None

def test_create_pelicula_and_informar_director_completo():
    director = Director("Peter Jackson", 9)
    pelicula = Pelicula("El señor de los anillos", "Sauron es muy malo", director)

    assert pelicula.titulo == "El señor de los anillos"
    assert pelicula.sinopsis == "Sauron es muy malo"
    assert pelicula._id_director == 9
    assert pelicula.id == -1
    assert pelicula.director == director

def test_asigna_director_a_pelicula():
    pelicula = Pelicula("El señor de los anillos", "Sauron es muy malo", -1)

    director = Director("Peter Jackson", 9)

    pelicula.director = director

    assert pelicula.titulo == "El señor de los anillos"
    assert pelicula.sinopsis == "Sauron es muy malo"
    assert pelicula.id == -1
    assert pelicula.director == director
    assert pelicula._id_director == 9

def test_dao_peliculas_traer_todos():
    dao = DAO_CSV_Pelicula("tests/data/peliculas.csv")
    peliculas = dao.todos()

    assert len(peliculas) == 5

    assert peliculas[1] == Pelicula("Los siete samurais", "Una banda de forajidos atemorizan a los habitantes de un pequeño pueblo, saqueándolos periódicamente sin piedad. Para repeler estos ataques, los aldeanos deciden contratar a mercenarios. Finalmente, consiguen los servicios de 7 guerreros, 7 samurais dispuestos a defenderlos a cambio, tan solo, de cobijo y comida.", 2, 17)

#Tests Genero
def test_create_genero():
    genero = Genero("Comedia")

    assert genero.genero == "Comedia"
    assert genero.id == -1

def test_dao_generos_traer_todos():
    dao = DAO_CSV_Genero("tests/data/generos.csv")
    generos = dao.todos()

    assert len(generos) == 13
    assert generos[0] == Genero("Accion", 1)

def test_create_genero_with_id():
    genero = Genero("Drama", 6)

    assert genero.genero == "Drama"
    assert genero.id == 6

def test_genero_igualdad():
    genero1 = Genero("Romantica", 10)
    genero2 = Genero("Romantica", 10)
    genero3 = Genero("Thriller", 12)

    assert genero1 == genero2
    assert genero1 != genero3

def test_genero_repr():
    genero = Genero("Western", 13)
    assert repr(genero) == "Genero (13): Western"

def test_dao_genero_create_from_dict():
    diccionario = {"genero": "Ciencia Ficcion", "id": "14"}
    genero = Genero.create_from_dict(diccionario)

    assert genero.genero == "Ciencia Ficcion"
    assert genero.id == 14

def test_asigna_genero_a_pelicula():
    pelicula = Pelicula("El señor de los anillos", "Sauron es muy malo", -1)
    genero = Genero("Aventura", 3)
    
    pelicula.genero = genero

    assert pelicula.titulo == "El señor de los anillos"
    assert pelicula.sinopsis == "Sauron es muy malo"
    assert pelicula.id == -1
    assert pelicula.genero == genero
    assert pelicula._id_genero == 3
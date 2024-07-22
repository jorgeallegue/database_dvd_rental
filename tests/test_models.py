from models.main_model import Director, DAO_CSV_Director, Pelicula, DAO_CSV_Pelicula, Genero, DAO_CSV_Genero, Copia, DAO_CSV_Copia

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

    assert len(peliculas) == 4

    assert peliculas[1] == Pelicula("Los siete samurais", "Una banda de forajidos atemorizan a los habitantes de un pequeño pueblo, saqueandolos periodicamente sin piedad. Para repeler estos ataques, los aldeanos deciden contratar a mercenarios. Finalmente, consiguen los servicios de 7 guerreros, 7 samurais dispuestos a defenderlos a cambio, tan solo, de cobijo y comida.", 2, 17 )

# Nuevas pruebas para Genero
def test_create_genero():
    genero = Genero("Comedia", 4)

    assert genero.genero == "Comedia"
    assert genero.id == 4

def test_dao_generos_traer_todos():
    dao = DAO_CSV_Genero("tests/data/generos.csv")
    generos = dao.todos()

    assert len(generos) == 13
    assert generos[0] == Genero("Accion", 1)

# Nuevas pruebas para Copia
def test_create_copia():
    copia = Copia(1, 1)

    assert copia.id_pelicula == 1
    assert copia.id == 1

def test_dao_copias_traer_todos():
    dao = DAO_CSV_Copia("tests/data/copias.csv")
    copias = dao.todos()

    assert len(copias) == 309
    assert copias[0] == Copia(1, 1)

# Pruebas para métodos CRUD en DAO_CSV
def test_dao_consultar_director():
    dao = DAO_CSV_Director("tests/data/directores.csv")
    director = dao.consultar(1)

    assert director == Director("Aditya Chopra", 1)

def test_dao_guardar_director():
    dao = DAO_CSV_Director("tests/data/directores.csv")
    nuevo_director = Director("Nuevo Director", 9)
    dao.guardar(nuevo_director)
    directores = dao.todos()

    assert nuevo_director in directores

def test_dao_borrar_director():
    dao = DAO_CSV_Director("tests/data/directores.csv")
    dao.borrar(9)
    directores = dao.todos()

    assert Director("Nuevo Director", 9) not in directores

def test_dao_actualizar_director():
    dao = DAO_CSV_Director("tests/data/directores.csv")
    director_actualizado = Director("Director Actualizado", 1)
    dao.actualizar(director_actualizado)
    director = dao.consultar(1)

    assert director == director_actualizado
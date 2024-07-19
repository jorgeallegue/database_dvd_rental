from models.main_model import Director, DAO_CSV_Director

def test_create_director():
    director = Director("Robert Redford")

    assert director.nombre == "Robert Redford"
    assert director.id == -1

def test_dao_directores_traer_findAll():
    dao = DAO_CSV_Director("tests/data/directores.csv")
    directores = dao.findAll()

    assert len(directores) == 8
    assert directores[7] == Director("Charlie Chaplin", 8)
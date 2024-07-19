from models.main_model import Director

def test_create_director():
    director = Director("Robert Redford")

    assert director.nombre == "Robert Redford"
    assert director.id == -1
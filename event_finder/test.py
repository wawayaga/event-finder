from event_finder import routes

def test_get_coordinates():
    #result = routes.get_coordinates("Carrer de Montcada, 25, Ciutat Vella, 08003 Barcelona, España")
    #assert result == [41.384990011183476, 2.1816517553237764]
    #result = routes.get_coordinates("Oranienstraße 19A, 10999 Berlin, Alemania")
    #assert result == [52.50081094550363, 13.422184611945935]
    result = routes.get_coordinates(None)
    assert result == None

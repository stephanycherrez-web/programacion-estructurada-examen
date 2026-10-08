import pytest
from cola import Cola


def test_cola_inicia_vacia():
    cola = Cola()
    assert cola.esta_vacia()


def test_encolar_aumenta_cantidad():
    cola = Cola()
    cola.encolar("A")
    assert cola.cantidad() == 1


def test_frente_devuelve_primero():
    cola = Cola()
    cola.encolar("A")
    cola.encolar("B")
    assert cola.frente() == "A"


def test_desencolar_respeta_fifo():
    cola = Cola()
    cola.encolar("A")
    cola.encolar("B")
    assert cola.desencolar() == "A"
    assert cola.desencolar() == "B"


def test_desencolar_vacia_genera_error():
    cola = Cola()
    with pytest.raises(IndexError):
        cola.desencolar()


def test_frente_vacia_genera_error():
    cola = Cola()
    with pytest.raises(IndexError):
        cola.frente()

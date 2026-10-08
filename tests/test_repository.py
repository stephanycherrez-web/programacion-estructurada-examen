import pytest
from producto import Producto
from repository import ProductoRepository


def crear_producto():
    return Producto("P001", "Teclado", 25.0, 5, "Accesorios")


def test_guardar_y_buscar_producto(tmp_path):
    repo = ProductoRepository(tmp_path / "productos.json")
    producto = crear_producto()
    repo.guardar(producto)
    encontrado = repo.buscar("P001")
    assert encontrado is not None
    assert encontrado.nombre == "Teclado"


def test_no_permite_sku_repetido(tmp_path):
    repo = ProductoRepository(tmp_path / "productos.json")
    repo.guardar(crear_producto())

    with pytest.raises(ValueError):
        repo.guardar(crear_producto())


def test_eliminar_producto(tmp_path):
    repo = ProductoRepository(tmp_path / "productos.json")
    repo.guardar(crear_producto())
    repo.eliminar("P001")
    assert repo.buscar("P001") is None


def test_persistencia_recupera_datos(tmp_path):
    archivo = tmp_path / "productos.json"

    repo1 = ProductoRepository(archivo)
    repo1.guardar(crear_producto())

    repo2 = ProductoRepository(archivo)
    recuperado = repo2.buscar("P001")

    assert recuperado is not None
    assert recuperado.nombre == "Teclado"

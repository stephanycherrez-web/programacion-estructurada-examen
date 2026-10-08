import json
from pathlib import Path
from producto import Producto


class ProductoRepository:
    def __init__(self, archivo="productos.json"):
        self.archivo = Path(archivo)
        self._productos = {}
        self._cargar()

    def _cargar(self):
        if not self.archivo.exists():
            self._productos = {}
            return

        try:
            contenido = self.archivo.read_text(encoding="utf-8").strip()
            if not contenido:
                self._productos = {}
                return

            datos = json.loads(contenido)
            self._productos = {
                item["sku"]: Producto.from_dict(item)
                for item in datos
            }
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            self._productos = {}

    def _guardar_archivo(self):
        datos = [p.to_dict() for p in self._productos.values()]
        self.archivo.write_text(
            json.dumps(datos, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    def guardar(self, producto):
        if producto.sku in self._productos:
            raise ValueError("Ya existe un producto con ese SKU")
        self._productos[producto.sku] = producto
        self._guardar_archivo()

    def buscar(self, sku):
        return self._productos.get(str(sku).strip())

    def actualizar(self, producto):
        if producto.sku not in self._productos:
            raise ValueError("No existe un producto con ese SKU")
        self._productos[producto.sku] = producto
        self._guardar_archivo()

    def eliminar(self, sku):
        sku = str(sku).strip()
        if sku not in self._productos:
            raise ValueError("No existe un producto con ese SKU")
        producto = self._productos.pop(sku)
        self._guardar_archivo()
        return producto

    def listar(self):
        return list(self._productos.values())

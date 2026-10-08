class Producto:
    def __init__(self, sku, nombre, precio, stock, categoria):
        self.sku = str(sku).strip()
        self.nombre = str(nombre).strip()
        self.precio = float(precio)
        self.stock = int(stock)
        self.categoria = str(categoria).strip()

    def to_dict(self):
        return {
            "sku": self.sku,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "categoria": self.categoria
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos["sku"],
            datos["nombre"],
            datos["precio"],
            datos["stock"],
            datos["categoria"]
        )

    def __str__(self):
        return f"{self.sku} | {self.nombre} | ${self.precio:.2f} | Stock: {self.stock} | {self.categoria}"

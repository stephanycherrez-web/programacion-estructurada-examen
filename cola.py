class Cola:
    def __init__(self):
        self._elementos = []

    def encolar(self, elemento):
        self._elementos.append(elemento)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._elementos.pop(0)

    def frente(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._elementos[0]

    def esta_vacia(self):
        return len(self._elementos) == 0

    def cantidad(self):
        return len(self._elementos)

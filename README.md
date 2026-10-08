# Catálogo de Productos

## Descripción
Este proyecto fue desarrollado en Python para la materia de Programación Estructurada. Permite registrar y administrar productos mediante una interfaz gráfica.

## Objetivo
Aplicar los conocimientos vistos durante la asignatura mediante clases, estructuras de datos, persistencia, interfaz gráfica, patrón Repository y pruebas.

## Funcionalidades
- Registrar productos.
- Buscar productos por SKU.
- Actualizar productos.
- Eliminar productos.
- Listar productos.
- Persistencia de datos con archivo JSON.
- Cola FIFO.
- Patrón Repository.
- Interfaz gráfica con Tkinter.
- Pruebas con pytest.

## Estructura
- `producto.py`: clase Producto.
- `cola.py`: cola FIFO.
- `repository.py`: persistencia y acceso a datos.
- `main.py`: interfaz gráfica.
- `productos.json`: datos persistentes.
- `tests/`: pruebas unitarias.

## Cómo ejecutar
```bash
py main.py
```

## Cómo ejecutar las pruebas
```bash
py -m pytest -v
```

## Lenguaje utilizado
Python.

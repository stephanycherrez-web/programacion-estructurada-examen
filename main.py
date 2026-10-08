import tkinter as tk
from tkinter import ttk, messagebox

from producto import Producto
from cola import Cola
from repository import ProductoRepository


class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Catálogo de Productos")
        self.root.geometry("900x600")

        self.repositorio = ProductoRepository("productos.json")
        self.cola = Cola()

        self.crear_interfaz()
        self.actualizar_tabla()

    def crear_interfaz(self):
        titulo = tk.Label(
            self.root,
            text="Catálogo de Productos",
            font=("Arial", 22, "bold")
        )
        titulo.pack(pady=10)

        subtitulo = tk.Label(
            self.root,
            text="Programación Estructurada - Persistencia, Repository, Cola FIFO e Interfaz Gráfica"
        )
        subtitulo.pack()

        formulario = tk.Frame(self.root)
        formulario.pack(pady=15)

        tk.Label(formulario, text="SKU").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(formulario, text="Nombre").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(formulario, text="Precio").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(formulario, text="Stock").grid(row=0, column=3, padx=5, pady=5)
        tk.Label(formulario, text="Categoría").grid(row=0, column=4, padx=5, pady=5)

        self.sku = tk.Entry(formulario, width=15)
        self.nombre = tk.Entry(formulario, width=22)
        self.precio = tk.Entry(formulario, width=12)
        self.stock = tk.Entry(formulario, width=12)
        self.categoria = tk.Entry(formulario, width=18)

        self.sku.grid(row=1, column=0, padx=5)
        self.nombre.grid(row=1, column=1, padx=5)
        self.precio.grid(row=1, column=2, padx=5)
        self.stock.grid(row=1, column=3, padx=5)
        self.categoria.grid(row=1, column=4, padx=5)

        botones = tk.Frame(self.root)
        botones.pack(pady=10)

        tk.Button(botones, text="Agregar", width=12, command=self.agregar).grid(row=0, column=0, padx=5)
        tk.Button(botones, text="Buscar", width=12, command=self.buscar).grid(row=0, column=1, padx=5)
        tk.Button(botones, text="Actualizar", width=12, command=self.actualizar).grid(row=0, column=2, padx=5)
        tk.Button(botones, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=3, padx=5)
        tk.Button(botones, text="Limpiar", width=12, command=self.limpiar).grid(row=0, column=4, padx=5)

        self.estado_cola = tk.Label(self.root, text="Productos pendientes en cola: 0")
        self.estado_cola.pack(pady=5)

        tk.Button(
            self.root,
            text="Procesar siguiente de la cola",
            command=self.procesar_cola
        ).pack(pady=5)

        columnas = ("sku", "nombre", "precio", "stock", "categoria")
        self.tabla = ttk.Treeview(self.root, columns=columnas, show="headings", height=14)

        self.tabla.heading("sku", text="SKU")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")
        self.tabla.heading("categoria", text="Categoría")

        self.tabla.column("sku", width=100)
        self.tabla.column("nombre", width=220)
        self.tabla.column("precio", width=100)
        self.tabla.column("stock", width=100)
        self.tabla.column("categoria", width=180)

        self.tabla.pack(fill="both", expand=True, padx=20, pady=15)

    def obtener_producto_formulario(self):
        if not all([
            self.sku.get().strip(),
            self.nombre.get().strip(),
            self.precio.get().strip(),
            self.stock.get().strip(),
            self.categoria.get().strip()
        ]):
            raise ValueError("Complete todos los campos")

        precio = float(self.precio.get())
        stock = int(self.stock.get())

        if precio < 0 or stock < 0:
            raise ValueError("Precio y stock no pueden ser negativos")

        return Producto(
            self.sku.get(),
            self.nombre.get(),
            precio,
            stock,
            self.categoria.get()
        )

    def agregar(self):
        try:
            producto = self.obtener_producto_formulario()
            self.repositorio.guardar(producto)
            self.cola.encolar(producto)
            self.estado_cola.config(
                text=f"Productos pendientes en cola: {self.cola.cantidad()}"
            )
            self.actualizar_tabla()
            self.limpiar()
            messagebox.showinfo("Correcto", "Producto agregado y guardado correctamente")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def buscar(self):
        sku = self.sku.get().strip()
        if not sku:
            messagebox.showwarning("Aviso", "Ingrese un SKU para buscar")
            return

        producto = self.repositorio.buscar(sku)

        if producto is None:
            messagebox.showwarning("Aviso", "Producto no encontrado")
            return

        self.nombre.delete(0, tk.END)
        self.precio.delete(0, tk.END)
        self.stock.delete(0, tk.END)
        self.categoria.delete(0, tk.END)

        self.nombre.insert(0, producto.nombre)
        self.precio.insert(0, str(producto.precio))
        self.stock.insert(0, str(producto.stock))
        self.categoria.insert(0, producto.categoria)

    def actualizar(self):
        try:
            producto = self.obtener_producto_formulario()
            self.repositorio.actualizar(producto)
            self.actualizar_tabla()
            messagebox.showinfo("Correcto", "Producto actualizado correctamente")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def eliminar(self):
        sku = self.sku.get().strip()
        if not sku:
            messagebox.showwarning("Aviso", "Ingrese un SKU para eliminar")
            return

        try:
            self.repositorio.eliminar(sku)
            self.actualizar_tabla()
            self.limpiar()
            messagebox.showinfo("Correcto", "Producto eliminado correctamente")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def limpiar(self):
        self.sku.delete(0, tk.END)
        self.nombre.delete(0, tk.END)
        self.precio.delete(0, tk.END)
        self.stock.delete(0, tk.END)
        self.categoria.delete(0, tk.END)

    def procesar_cola(self):
        if self.cola.esta_vacia():
            messagebox.showwarning("Aviso", "No hay productos pendientes en la cola")
            return

        producto = self.cola.desencolar()
        self.estado_cola.config(
            text=f"Productos pendientes en cola: {self.cola.cantidad()}"
        )
        messagebox.showinfo(
            "Cola FIFO",
            f"Producto procesado: {producto.nombre}"
        )

    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for producto in self.repositorio.listar():
            self.tabla.insert(
                "",
                tk.END,
                values=(
                    producto.sku,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.stock,
                    producto.categoria
                )
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

#José Campodonico
#Nicolás Vergara
import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# --- CONEXIÓN ---
def conectar():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "Base_de_datos", "w1.db")
    db_path = os.path.normpath(db_path)
    return sqlite3.connect(db_path)

# --- INICIALIZACIÓN DE LA VENTANA PRINCIPAL ---
root = tk.Tk()
root.title("Finis TCGrrae - Gestión Completa")
root.geometry("1150x780")
root.configure(bg="#f5f5f5")

# --- CONFIGURACIÓN DE PESTAÑAS ---
tab_control = ttk.Notebook(root)
tab_inventario = ttk.Frame(tab_control)
tab_carrito = ttk.Frame(tab_control)
tab_ventas = ttk.Frame(tab_control)
tab_recepcion = ttk.Frame(tab_control)  

tab_control.add(tab_inventario, text="Inventario")
tab_control.add(tab_carrito, text="Carrito de Compras")
tab_control.add(tab_ventas, text="Ventas Realizadas")
tab_control.add(tab_recepcion, text="Recepción de Stock")  
tab_control.pack(expand=1, fill="both")

# --- PESTAÑA INVENTARIO ---
tk.Label(tab_inventario, text="Inventario por Estante", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

tree_inv = ttk.Treeview(tab_inventario, columns=("ID", "Nombre", "Precio", "Stock", "Estante"), show="headings", height=20)
tree_inv.heading("ID", text="ID")
tree_inv.heading("Nombre", text="Nombre")
tree_inv.heading("Precio", text="Precio")
tree_inv.heading("Stock", text="Stock")
tree_inv.heading("Estante", text="Estante")
tree_inv.column("ID", width=60, anchor="center")
tree_inv.column("Nombre", width=380)
tree_inv.column("Precio", width=100, anchor="e")
tree_inv.column("Stock", width=80, anchor="center")
tree_inv.column("Estante", width=120, anchor="center")
tree_inv.pack(padx=20, pady=10, fill="both", expand=True)

def cargar_inventario():
    for row in tree_inv.get_children():
        tree_inv.delete(row)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p."ID_Producto", p."Nombre", p."Precio", i."Cantidad_disponible", i."Ubicacion"
        FROM "Producto" p
        JOIN "Inventario" i ON p."ID_Producto" = i."ID_Producto"
        ORDER BY i."Ubicacion", p."ID_Producto"
    ''')
    for row in cursor.fetchall():
        tree_inv.insert("", "end", values=row)
    conn.close()

btn_actualizar = tk.Button(tab_inventario, text="Actualizar Inventario", command=cargar_inventario, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_actualizar.pack(pady=5)

# --- PESTAÑA CARRITO ---
tk.Label(tab_carrito, text="Carrito de Compras", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)
frame_cliente = tk.LabelFrame(tab_carrito, text="Cliente", padx=10, pady=10, bg="#f5f5f5")
frame_cliente.pack(padx=20, pady=5, fill="x")
tk.Label(frame_cliente, text="ID Cliente:", bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5, sticky="e")
combo_cliente = ttk.Combobox(frame_cliente, width=50)
combo_cliente.grid(row=0, column=1, padx=5, pady=5)
frame_agregar = tk.LabelFrame(tab_carrito, text="Agregar Producto", padx=10, pady=10, bg="#f5f5f5")
frame_agregar.pack(padx=20, pady=5, fill="x")
tk.Label(frame_agregar, text="Producto:", bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5, sticky="e")
combo_producto = ttk.Combobox(frame_agregar, width=60)
combo_producto.grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_agregar, text="Cantidad:", bg="#f5f5f5").grid(row=0, column=2, padx=5, pady=5, sticky="e")
entry_cant = tk.Entry(frame_agregar, width=10)
entry_cant.insert(0, "1")
entry_cant.grid(row=0, column=3, padx=5, pady=5)

tree_carrito = ttk.Treeview(tab_carrito, columns=("ID", "Nombre", "Cant", "Precio", "Subtotal"), show="headings", height=8)
tree_carrito.heading("ID", text="ID")
tree_carrito.heading("Nombre", text="Producto")
tree_carrito.heading("Cant", text="Cant")
tree_carrito.heading("Precio", text="Precio")
tree_carrito.heading("Subtotal", text="Subtotal")
tree_carrito.column("ID", width=60, anchor="center")
tree_carrito.column("Nombre", width=380)
tree_carrito.column("Cant", width=80, anchor="center")
tree_carrito.column("Precio", width=110, anchor="e")
tree_carrito.column("Subtotal", width=130, anchor="e")
tree_carrito.pack(padx=20, pady=10, fill="x")

lbl_total = tk.Label(tab_carrito, text="Total: $0", font=("Arial", 14, "bold"), bg="#f5f5f5")
lbl_total.pack(pady=5)

frame_botones = tk.Frame(tab_carrito, bg="#f5f5f5")
frame_botones.pack(pady=10)
btn_agregar = tk.Button(frame_botones, text="Agregar al Carrito", bg="#2196F3", fg="white", width=20)
btn_agregar.grid(row=0, column=0, padx=10)
btn_finalizar = tk.Button(frame_botones, text="Finalizar Venta", bg="#FF5722", fg="white", width=20, state="disabled")
btn_finalizar.grid(row=0, column=1, padx=10)
btn_limpiar = tk.Button(frame_botones, text="Limpiar Carrito", bg="#9E9E9E", fg="white", width=20)
btn_limpiar.grid(row=0, column=2, padx=10)

# --- PESTAÑA VENTAS REALIZADAS ---
tk.Label(tab_ventas, text="Historial de Ventas", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

tree_ventas = ttk.Treeview(tab_ventas, columns=("ID", "Fecha", "Cliente", "Total", "Productos"), show="headings", height=20)
tree_ventas.heading("ID", text="ID Venta")
tree_ventas.heading("Fecha", text="Fecha")
tree_ventas.heading("Cliente", text="Cliente")
tree_ventas.heading("Total", text="Total")
tree_ventas.heading("Productos", text="Productos")
tree_ventas.column("ID", width=80, anchor="center")
tree_ventas.column("Fecha", width=120, anchor="center")
tree_ventas.column("Cliente", width=200)
tree_ventas.column("Total", width=130, anchor="e")
tree_ventas.column("Productos", width=400)
tree_ventas.pack(padx=20, pady=10, fill="both", expand=True)

btn_actualizar_ventas = tk.Button(tab_ventas, text="Actualizar Ventas", command=lambda: cargar_ventas(), bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_actualizar_ventas.pack(pady=5)

# --- PESTAÑA RECEPCIÓN DE STOCK ---
tk.Label(tab_recepcion, text="Recepción de Stock", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=15)

frame_recepcion = tk.LabelFrame(tab_recepcion, text="Ingresar Productos al Inventario", padx=15, pady=15, bg="#f5f5f5")
frame_recepcion.pack(padx=30, pady=10, fill="x")

tk.Label(frame_recepcion, text="Producto:", bg="#f5f5f5", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=8, sticky="e")
combo_producto_stock = ttk.Combobox(frame_recepcion, width=60, font=("Arial", 10))
combo_producto_stock.grid(row=0, column=1, padx=10, pady=8)

tk.Label(frame_recepcion, text="Cantidad Recibida:", bg="#f5f5f5", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=8, sticky="e")
entry_cant_stock = tk.Entry(frame_recepcion, width=15, font=("Arial", 10))
entry_cant_stock.insert(0, "1")
entry_cant_stock.grid(row=1, column=1, padx=10, pady=8, sticky="w")

tk.Label(frame_recepcion, text="Proveedor (opcional):", bg="#f5f5f5", font=("Arial", 11)).grid(row=2, column=0, padx=10, pady=8, sticky="e")
combo_proveedor = ttk.Combobox(frame_recepcion, width=40, font=("Arial", 10))
combo_proveedor.grid(row=2, column=1, padx=10, pady=8, sticky="w")

btn_recepcion = tk.Button(frame_recepcion, text="Recibir Stock", bg="#8BC34A", fg="white", font=("Arial", 11, "bold"), width=20)
btn_recepcion.grid(row=3, column=0, columnspan=2, pady=15)

lbl_mensaje_stock = tk.Label(tab_recepcion, text="", font=("Arial", 11), bg="#f5f5f5", fg="#2E7D32")
lbl_mensaje_stock.pack(pady=5)

# --- LÓGICA DEL CARRITO Y FUNCIONES ---
carrito = []

def cargar_combos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT "ID_Cliente", "Nombre" FROM "Cliente" ORDER BY "ID_Cliente"')
    clientes = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
    combo_cliente['values'] = clientes
    combo_producto_stock['values'] = clientes 

    cursor.execute('SELECT "ID_Producto", "Nombre" FROM "Producto" ORDER BY "ID_Producto"')
    productos = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
    combo_producto['values'] = productos
    combo_producto_stock['values'] = productos

    cursor.execute('SELECT "ID_Proveedor", "Nombre" FROM "Proveedor" ORDER BY "ID_Proveedor"')
    proveedores = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
    combo_proveedor['values'] = proveedores
    conn.close()

def actualizar_carrito():
    for row in tree_carrito.get_children():
        tree_carrito.delete(row)
    total = 0
    for item in carrito:
        subtotal = item['cant'] * item['precio']
        total += subtotal
        tree_carrito.insert("", "end", values=(item['id'], item['nombre'], item['cant'], f"${item['precio']:,}", f"${subtotal:,}"))
    lbl_total.config(text=f"Total: ${total:,}")
    btn_finalizar.config(state="normal" if carrito and combo_cliente.get() else "disabled")

def agregar_al_carrito():
    prod_text = combo_producto.get()
    try:
        cant = int(entry_cant.get())
    except:
        messagebox.showerror("Error", "Cantidad inválida")
        return
    if not prod_text or cant <= 0:
        messagebox.showerror("Error", "Selecciona producto y cantidad")
        return

    id_prod = int(prod_text.split(" - ")[0])
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT "Nombre", "Precio", "Cantidad_disponible" FROM "Producto" p JOIN "Inventario" i ON p."ID_Producto" = i."ID_Producto" WHERE p."ID_Producto" = ?', (id_prod,))
    row = cursor.fetchone()
    if not row: 
        conn.close()
        return
    nombre, precio, stock = row
    conn.close()

    for item in carrito:
        if item['id'] == id_prod:
            item['cant'] += cant
            actualizar_carrito()
            entry_cant.delete(0, tk.END)
            entry_cant.insert(0, "1")
            return

    carrito.append({'id': id_prod, 'nombre': nombre, 'precio': precio, 'cant': cant})
    actualizar_carrito()
    entry_cant.delete(0, tk.END)
    entry_cant.insert(0, "1")

def finalizar_venta():
    cliente_text = combo_cliente.get()
    if not cliente_text or not carrito:
        messagebox.showerror("Error", "Selecciona cliente y agrega productos")
        return

    id_cliente = int(cliente_text.split(" - ")[0])
    conn = conectar()
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO "Venta" ("Fecha", "Tipo_de_venta", "Estado", "Tipo_de_documento", "ID_Tienda", "ID_Cliente", "ID_Empleado", "Total")
        VALUES (?, 'Presencial', 'Completado', 'Boleta', 1, ?, 3, 0)
    ''', (fecha, id_cliente))
    id_venta = cursor.lastrowid

    total_venta = 0
    productos_lista = []
    for item in carrito:
        subtotal = item['cant'] * item['precio']
        total_venta += subtotal
        productos_lista.append(f"{item['cant']}x {item['nombre']}")
        cursor.execute('''
            INSERT INTO "Linea_de_venta" ("Cantidad", "Precio_Unitario", "ID_Venta", "ID_Producto")
            VALUES (?, ?, ?, ?)
        ''', (item['cant'], item['precio'], id_venta, item['id']))
        cursor.execute('UPDATE "Producto" SET "Stock" = "Stock" - ? WHERE "ID_Producto" = ?', (item['cant'], item['id']))
        cursor.execute('UPDATE "Inventario" SET "Cantidad_disponible" = "Cantidad_disponible" - ? WHERE "ID_Producto" = ?', (item['cant'], item['id']))

    cursor.execute('UPDATE "Venta" SET "Total" = ? WHERE "ID_Venta" = ?', (total_venta, id_venta))
    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", f"Venta #{id_venta} registrada por ${total_venta:,}\nProductos: {', '.join(productos_lista)}")
    carrito.clear()
    actualizar_carrito()
    cargar_inventario()
    cargar_ventas()

def limpiar_carrito():
    carrito.clear()
    actualizar_carrito()

def cargar_ventas():
    for row in tree_ventas.get_children():
        tree_ventas.delete(row)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT v."ID_Venta", v."Fecha", c."Nombre", v."Total"
        FROM "Venta" v
        JOIN "Cliente" c ON v."ID_Cliente" = c."ID_Cliente"
        ORDER BY v."ID_Venta" DESC
    ''')
    ventas = cursor.fetchall()
    for venta in ventas:
        id_venta = venta[0]
        cursor.execute('''
            SELECT p."Nombre", l."Cantidad"
            FROM "Linea_de_venta" l
            JOIN "Producto" p ON l."ID_Producto" = p."ID_Producto"
            WHERE l."ID_Venta" = ?
        ''', (id_venta,))
        productos = [f"{row[1]}x {row[0]}" for row in cursor.fetchall()]
        productos_str = ", ".join(productos) if productos else "Ninguno"
        tree_ventas.insert("", "end", values=(venta[0], venta[1], venta[2], f"${venta[3]:,}", productos_str))
    conn.close()

# --- LÓGICA RECEPCIÓN DE STOCK ---
def recibir_stock():
    prod_text = combo_producto_stock.get()
    try:
        cant = int(entry_cant_stock.get())
    except:
        messagebox.showerror("Error", "Cantidad inválida")
        return
    if not prod_text or cant <= 0:
        messagebox.showerror("Error", "Selecciona producto y cantidad")
        return

    id_prod = int(prod_text.split(" - ")[0])
    conn = conectar()
    cursor = conn.cursor()

    # Actualizar stock
    cursor.execute('UPDATE "Producto" SET "Stock" = "Stock" + ? WHERE "ID_Producto" = ?', (cant, id_prod))
    cursor.execute('UPDATE "Inventario" SET "Cantidad_disponible" = "Cantidad_disponible" + ? WHERE "ID_Producto" = ?', (cant, id_prod))

    conn.commit()
    conn.close()

    lbl_mensaje_stock.config(text=f"Stock actualizado: +{cant} unidades del producto ID {id_prod}")
    cargar_inventario()
    entry_cant_stock.delete(0, tk.END)
    entry_cant_stock.insert(0, "1")

btn_recepcion.config(command=recibir_stock)

# --- INICIAR APLICACIÓN ---
cargar_inventario()
cargar_combos()
actualizar_carrito()
cargar_ventas()

# Asignar botones
btn_agregar.config(command=agregar_al_carrito)
btn_finalizar.config(command=finalizar_venta)
btn_limpiar.config(command=limpiar_carrito)

root.mainloop()

import flet as ft
from db_connection import get_connection
from functools import partial

def compra_view(page: ft.Page) -> ft.Control:
    page.title = "Compras"
    #Quito el scroll de toda la pagina pa

    fecha = ft.TextField(label="Fecha", width=150)
    proveedor = ft.TextField(label="Proveedor", width=150)
    observaciones = ft.TextField(label="Observaciones", width=300)
    tipo = ft.Dropdown(label="Tipo", options=[
        ft.dropdown.Option("aluminio", "Aluminio"),
        ft.dropdown.Option("cristal", "Cristal"),
        ft.dropdown.Option("herrajes", "Herrajes")
    ], width=150)
    id_producto = ft.TextField(label="ID Producto", width=100)
    cantidad = ft.TextField(label="Cantidad", width=100, keyboard_type=ft.KeyboardType.NUMBER)
    precio = ft.TextField(label="Precio Unitario", width=100, keyboard_type=ft.KeyboardType.NUMBER)

    detalles = []

    def agregar_detalle(e):
        if not tipo.value or not id_producto.value or not cantidad.value or not precio.value:
            return
        detalles.append({
            "tipo": tipo.value,
            "id": int(id_producto.value),
            "cantidad": float(cantidad.value),
            "precio": float(precio.value)
        })
        tipo.value = id_producto.value = cantidad.value = precio.value = ""

    def eliminar_detalle(index, e=None):
        detalles.pop(index)

    def guardar_compra(e):
        if not fecha.value or not proveedor.value or not detalles:
            return
        conn = get_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO compra (fecha, proveedor, observaciones) VALUES (%s, %s, %s)",
                    (fecha.value, proveedor.value, observaciones.value))
        id_compra = cur.lastrowid
        for d in detalles:
            tabla = f"detalle_compra_{d['tipo']}"
            fk = {"aluminio": "idAluminio", "cristal": "idCristal", "herrajes": "idHerrajes"}[d["tipo"]]
            cur.execute(
                f"INSERT INTO {tabla} (idCompra, {fk}, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                (id_compra, d["id"], d["cantidad"], d["precio"])
            )
            cur.execute(
                f"""INSERT INTO stock_{d['tipo']} ({fk}, cantidad)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE cantidad = cantidad + VALUES(cantidad)""",
                (d["id"], d["cantidad"])
            )
        conn.commit(); conn.close()
        detalles.clear()
        fecha.value = proveedor.value = observaciones.value = ""
        cargar_compras()
        page.update()

    # 🧹 Eliminar compra completa (incluye detalles)
    def eliminar_compra(id_compra):
        conn = get_connection(); cur = conn.cursor()
        cur.execute("DELETE FROM detalle_compra_aluminio WHERE idCompra = %s", (id_compra,))
        cur.execute("DELETE FROM detalle_compra_cristal WHERE idCompra = %s", (id_compra,))
        cur.execute("DELETE FROM detalle_compra_herrajes WHERE idCompra = %s", (id_compra,))
        cur.execute("DELETE FROM compra WHERE idCompra = %s", (id_compra,))
        conn.commit(); conn.close()
        cargar_compras()

    # 🧾 Tabla visual de compras
    tabla_compras = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Fecha")),
        ft.DataColumn(ft.Text("Proveedor")),
        ft.DataColumn(ft.Text("Observaciones")),
        ft.DataColumn(ft.Text("Eliminar"))
    ])

    def cargar_compras():
        tabla_compras.rows.clear()
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT idCompra, fecha, proveedor, observaciones FROM compra")
        for row in cur.fetchall():
            tabla_compras.rows.append(ft.DataRow([
                ft.DataCell(ft.Text(str(row[0]))),
                ft.DataCell(ft.Text(str(row[1]))),
                ft.DataCell(ft.Text(row[2])),
                ft.DataCell(ft.Text(row[3])),
                ft.DataCell(ft.IconButton(
                    icon=ft.Icons.DELETE,
                    tooltip="Eliminar",
                    on_click=lambda e, id=row[0]: eliminar_compra(id)
                ))
            ]))
        conn.close(); page.update()

    cargar_compras()

    return ft.Column([
        ft.Text("Registro de Compra", size=18, weight="bold"),
        ft.Row([fecha, proveedor, observaciones], wrap=True),
        ft.Row([
            tipo, id_producto, cantidad, precio,
            ft.ElevatedButton("Agregar Detalle", on_click=agregar_detalle)
        ], wrap=True),
        ft.ElevatedButton("Guardar Compra", on_click=guardar_compra),
        ft.Divider(),
        ft.Text("Compras Registradas", weight="bold"),
        ft.Container(
            content=ft.Column([tabla_compras], scroll=ft.ScrollMode.AUTO),
            height=400,
            padding=10
        )
    ])







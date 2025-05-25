import flet as ft
from db_connection import get_connection
from functools import partial

def venta_view(page: ft.Page) -> ft.Control:
    page.title = "Ventas"

    fecha = ft.TextField(label="Fecha", width=150)
    motivo = ft.TextField(label="Motivo", width=300)
    tipo = ft.Dropdown(label="Tipo", options=[
        ft.dropdown.Option("aluminio", "Aluminio"),
        ft.dropdown.Option("cristal", "Cristal"),
        ft.dropdown.Option("herrajes", "Herrajes")
    ], width=150)
    id_producto = ft.TextField(label="ID Producto", width=100)
    cantidad = ft.TextField(label="Cantidad", width=100, keyboard_type=ft.KeyboardType.NUMBER)

    detalles = []

    def agregar_detalle(e):
        if not tipo.value or not id_producto.value or not cantidad.value:
            return
        detalles.append({
            "tipo": tipo.value,
            "id": int(id_producto.value),
            "cantidad": float(cantidad.value)
        })
        tipo.value = id_producto.value = cantidad.value = ""

    def eliminar_detalle(index, e=None):
        detalles.pop(index)

    def guardar_venta(e):
        if not fecha.value or not detalles:
            return
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO salida (fecha, motivo) VALUES (%s, %s)", (fecha.value, motivo.value))
        id_salida = cur.lastrowid
        for d in detalles:
            tabla = f"detalle_salida_{d['tipo']}"
            fk = {"aluminio": "idAluminio", "cristal": "idCristal", "herrajes": "idHerrajes"}[d["tipo"]]
            cur.execute(
                f"INSERT INTO {tabla} (idSalida, {fk}, cantidad) VALUES (%s, %s, %s)",
                (id_salida, d["id"], d["cantidad"])
            )
            cur.execute(
                f"UPDATE stock_{d['tipo']} SET cantidad = cantidad - %s WHERE {fk} = %s",
                (d["cantidad"], d["id"])
            )
        conn.commit()
        conn.close()
        detalles.clear()
        fecha.value = motivo.value = ""
        cargar_ventas()
        page.update()

    def eliminar_venta(id_salida, e=None):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM detalle_salida_aluminio WHERE idSalida = %s", (id_salida,))
        cur.execute("DELETE FROM detalle_salida_cristal WHERE idSalida = %s", (id_salida,))
        cur.execute("DELETE FROM detalle_salida_herrajes WHERE idSalida = %s", (id_salida,))
        cur.execute("DELETE FROM salida WHERE idSalida = %s", (id_salida,))
        conn.commit()
        conn.close()
        cargar_ventas()

    tabla_ventas = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Fecha")),
        ft.DataColumn(ft.Text("Motivo")),
        ft.DataColumn(ft.Text("Eliminar"))
    ])

    def cargar_ventas():
        tabla_ventas.rows.clear()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT idSalida, fecha, motivo FROM salida")
        for row in cur.fetchall():
            tabla_ventas.rows.append(ft.DataRow([
                ft.DataCell(ft.Text(str(row[0]))),
                ft.DataCell(ft.Text(str(row[1]))),
                ft.DataCell(ft.Text(row[2])),
                ft.DataCell(ft.IconButton(
                    icon=ft.Icons.DELETE,
                    tooltip="Eliminar",
                    on_click=partial(eliminar_venta, row[0])
                ))
            ]))
        conn.close()
        page.update()

    cargar_ventas()

    return ft.Column([
        ft.Text("Registro de Venta", size=18, weight="bold"),
        ft.Row([fecha, motivo], wrap=True),
        ft.Row([
            tipo, id_producto, cantidad,
            ft.ElevatedButton("Agregar Detalle", on_click=agregar_detalle)
        ], wrap=True),
        ft.ElevatedButton("Guardar Venta", on_click=guardar_venta),
        ft.Divider(),
        ft.Text("Ventas Registradas", weight="bold"),
        ft.Container(
            content=ft.Column([tabla_ventas], scroll=ft.ScrollMode.AUTO),
            height=400,
            padding=10
        )
    ])






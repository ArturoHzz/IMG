import flet as ft
from db_connection import get_connection

def vidrio_view(page: ft.Page) -> ft.Control:
    page.title = "Vidrio"
    #Acuerdate w se quita esta madre

    # Filtros
    filtro_color = ft.Dropdown(label="Color", options=[], width=150)
    filtro_tipo = ft.Dropdown(label="Tipo", options=[], width=150)
    filtro_espesor = ft.Dropdown(label="Espesor", options=[], width=150)

    # Formulario de alta
    nuevo_color = ft.Dropdown(label="Color", options=[], width=150)
    nuevo_tipo = ft.Dropdown(label="Tipo", options=[], width=150)
    nuevo_espesor = ft.Dropdown(label="Espesor", options=[], width=150)
    nuevo_hoja = ft.Dropdown(label="Hoja", options=[
        ft.dropdown.Option("media", "Media"),
        ft.dropdown.Option("chica", "Chica"),
        ft.dropdown.Option("grande", "Grande"),
    ], width=150)
    nuevo_desc = ft.TextField(label="Descripción", width=200)

    # Tabla
    tabla = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Color")),
        ft.DataColumn(ft.Text("Tipo")),
        ft.DataColumn(ft.Text("Espesor")),
        ft.DataColumn(ft.Text("Hoja")),
        ft.DataColumn(ft.Text("Descripción")),
        ft.DataColumn(ft.Text("Eliminar")),
    ])

    # ───────────── FUNCIONES ─────────────
    def cargar_opciones():
        conn = get_connection()
        cur = conn.cursor()

        def asignar_opciones(query, controles):
            cur.execute(query)
            opciones = [ft.dropdown.Option(str(id), nombre) for id, nombre in cur.fetchall()]
            for c in controles:
                c.options = opciones.copy()

        asignar_opciones("SELECT idColor, nombre_color FROM color", [filtro_color, nuevo_color])
        asignar_opciones("SELECT idTipo_cristal, nombre_tipo FROM tipo_cristal", [filtro_tipo, nuevo_tipo])
        asignar_opciones("SELECT idEspesor, medida_mm FROM espesor", [filtro_espesor, nuevo_espesor])

        conn.close()
        page.update()

    def cargar_tabla(e=None):
        tabla.rows.clear()
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT c.idCristal, col.nombre_color, tip.nombre_tipo, esp.medida_mm,
                   c.tipo_hoja, c.descripcion
            FROM cristal c
            LEFT JOIN color col ON c.idColor = col.idColor
            LEFT JOIN tipo_cristal tip ON c.idTipo_cristal = tip.idTipo_cristal
            LEFT JOIN espesor esp ON c.idEspesor = esp.idEspesor
        """
        filtros, valores = [], []
        if filtro_color.value:
            filtros.append("c.idColor = %s")
            valores.append(filtro_color.value)
        if filtro_tipo.value:
            filtros.append("c.idTipo_cristal = %s")
            valores.append(filtro_tipo.value)
        if filtro_espesor.value:
            filtros.append("c.idEspesor = %s")
            valores.append(filtro_espesor.value)
        if filtros:
            query += " WHERE " + " AND ".join(filtros)

        cur.execute(query, valores)
        for row in cur.fetchall():
            tabla.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(row[0]))),
                ft.DataCell(ft.Text(row[1] or "")),
                ft.DataCell(ft.Text(row[2] or "")),
                ft.DataCell(ft.Text(str(row[3]))),
                ft.DataCell(ft.Text(row[4] or "")),
                ft.DataCell(ft.Text(row[5] or "")),
                ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=row[0]: eliminar(id)))
            ]))
        conn.close()
        page.update()

    def agregar_registro(e):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COALESCE(MAX(idCristal), 0) + 1 FROM cristal")
        nuevo_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO cristal (idCristal, idColor, idTipo_cristal, idEspesor, tipo_hoja, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            nuevo_id,
            int(nuevo_color.value),
            int(nuevo_tipo.value),
            int(nuevo_espesor.value),
            nuevo_hoja.value,
            nuevo_desc.value.strip()
        ))
        conn.commit()
        conn.close()
        cargar_tabla()

    def eliminar(id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM cristal WHERE idCristal = %s", (id,))
        conn.commit()
        conn.close()
        cargar_tabla()

    def limpiar_filtros(e):
        filtro_color.value = filtro_tipo.value = filtro_espesor.value = None
        cargar_tabla()

    # ───────────── DISEÑO DE LA VISTA ─────────────
    cargar_opciones()
    cargar_tabla()

    return ft.Column([
        ft.Text("Filtros", size=16, weight="bold"),
        ft.Row([filtro_color, filtro_tipo, filtro_espesor,
                ft.ElevatedButton("Buscar", on_click=cargar_tabla),
                ft.ElevatedButton("Limpiar", on_click=limpiar_filtros)], spacing=10),
        ft.Divider(),
        ft.Text("Agregar Nuevo Vidrio", size=16, weight="bold"),
        ft.Row([nuevo_color, nuevo_tipo, nuevo_espesor, nuevo_hoja, nuevo_desc,
                ft.ElevatedButton("Agregar", on_click=agregar_registro)], spacing=10),
        ft.Divider(),
        ft.Text("Registros de Vidrio", size=16, weight="bold"),
        ft.Container(
            content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
            height=400,  # Altura fija para la tabla
            padding=10
        )
    ])




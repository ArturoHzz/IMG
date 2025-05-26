
import flet as ft
from db_connection import get_connection

# ========================= HERREJES =========================
def herrajes_view(page: ft.Page) -> ft.Control:
    page.title = "Herrajes"

    filtros = {
        'carretas': ft.Dropdown(label="Carretas", options=[], width=150),
        'jaladeras': ft.Dropdown(label="Jaladeras", options=[], width=150),
        'chapa': ft.Dropdown(label="Chapa", options=[], width=150),
        'bisagras': ft.Dropdown(label="Bisagras", options=[], width=150),
        'color': ft.Dropdown(label="Color", options=[], width=150),
    }

    nuevos = {
        k: ft.Dropdown(label=dd.label, options=[], width=150) for k, dd in filtros.items()
    }

    tabla = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        *[ft.DataColumn(ft.Text(dd.label)) for dd in filtros.values()],
        ft.DataColumn(ft.Text("Eliminar")),
    ])

    def cargar_opciones():
        conn = get_connection(); cur = conn.cursor()
        dropdowns = [
            ("SELECT idCarretas, nombre_carretas FROM carretas", 'carretas'),
            ("SELECT idJaladeras, tipo_jaladeras FROM jaladeras", 'jaladeras'),
            ("SELECT idChapa, tipo_chapa FROM chapa", 'chapa'),
            ("SELECT idBisagras, tipo_bisagra FROM bisagras", 'bisagras'),
            ("SELECT idColor, nombre_color FROM color", 'color'),
        ]
        for query, key in dropdowns:
            cur.execute(query)
            opciones = [ft.dropdown.Option(str(i), n) for i, n in cur.fetchall()]
            filtros[key].options = opciones.copy()
            nuevos[key].options = opciones.copy()
        conn.close(); page.update()

    def cargar(e=None):
        tabla.rows.clear()
        conn = get_connection(); cur = conn.cursor()
        sql = """
            SELECT h.idHerrajes, ca.nombre_carretas, ja.tipo_jaladeras, ch.tipo_chapa,
                b.tipo_bisagra, co.nombre_color
            FROM herrajes h
            LEFT JOIN carretas ca ON h.idCarretas = ca.idCarretas
            LEFT JOIN jaladeras ja ON h.idJaladeras = ja.idJaladeras
            LEFT JOIN chapa ch ON h.idChapa = ch.idChapa
            LEFT JOIN bisagras b ON h.idBisagras = b.idBisagras
            LEFT JOIN color co ON h.idColor = co.idColor
        """

        condiciones = []
        valores = []

        if filtros['carretas'].value:
            condiciones.append("h.idCarretas = %s")
            valores.append(filtros['carretas'].value)
        if filtros['jaladeras'].value:
            condiciones.append("h.idJaladeras = %s")
            valores.append(filtros['jaladeras'].value)
        if filtros['chapa'].value:
            condiciones.append("h.idChapa = %s")
            valores.append(filtros['chapa'].value)
        if filtros['bisagras'].value:
            condiciones.append("h.idBisagras = %s")
            valores.append(filtros['bisagras'].value)
        if filtros['color'].value:
            condiciones.append("h.idColor = %s")
            valores.append(filtros['color'].value)

        if condiciones:
            sql += " WHERE " + " AND ".join(condiciones)

        cur.execute(sql, valores)
        for row in cur.fetchall():
            tabla.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(row[0]))),
                *[ft.DataCell(ft.Text(str(val) or "")) for val in row[1:]],
                ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=row[0]: eliminar(id)))
            ]))
        conn.close(); page.update()

    def limpiar_filtros(e=None):
        for dd in filtros.values():
            dd.value = None
        cargar()

    def agregar(e):
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT COALESCE(MAX(idHerrajes), 0)+1 FROM herrajes")
        nuevo_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO herrajes (idHerrajes, idCarretas, idJaladeras, idChapa, idBisagras, idColor)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, [nuevo_id] + [int(nuevos[k].value) for k in ['carretas','jaladeras','chapa','bisagras','color']])
        conn.commit(); conn.close(); cargar()

    def eliminar(id):
        conn = get_connection(); cur = conn.cursor()
        cur.execute("DELETE FROM herrajes WHERE idHerrajes=%s", (id,))
        conn.commit(); conn.close(); cargar()

    cargar_opciones(); cargar()

    return ft.Column([
        ft.Text("Filtros y Agregado de Herrajes", size=18, weight="bold"),
        ft.Row(
            list(filtros.values()) + [
                ft.ElevatedButton("Buscar", on_click=cargar),
                ft.ElevatedButton("Limpiar", on_click=limpiar_filtros)
            ],
            wrap=True
        ),
        ft.Divider(),
        ft.Row(list(nuevos.values()) + [ft.ElevatedButton("Agregar", on_click=agregar)], wrap=True),
        ft.Divider(),
        ft.Container(
            content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
            height=400,
            padding=10
        )
    ])





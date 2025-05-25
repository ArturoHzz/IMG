import flet as ft
from db_connection import get_connection

def stock_view(page: ft.Page) -> ft.Control:
    page.title = "Stock"
    page.scroll = ft.ScrollMode.AUTO

    # Tablas
    tabla_aluminio = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Descripción")),
        ft.DataColumn(ft.Text("Cantidad"))
    ])
    tabla_cristal = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Descripción")),
        ft.DataColumn(ft.Text("Cantidad"))
    ])
    tabla_herrajes = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Descripción")),
        ft.DataColumn(ft.Text("Cantidad"))
    ])

    # Filtros Aluminio
    filtro_perfil = ft.Dropdown(label="Perfil", options=[], width=150)
    filtro_color_alu = ft.Dropdown(label="Color", options=[], width=150)
    filtro_serie = ft.Dropdown(label="Serie", options=[], width=150)

    # Filtros Cristal
    filtro_tipo = ft.Dropdown(label="Tipo", options=[], width=150)
    filtro_color_cri = ft.Dropdown(label="Color", options=[], width=150)
    filtro_espesor = ft.Dropdown(label="Espesor", options=[], width=150)

    # Filtros Herrajes
    filtro_carretas = ft.Dropdown(label="Carretas", options=[], width=150)
    filtro_color_her = ft.Dropdown(label="Color", options=[], width=150)

    def cargar_opciones():
        conn = get_connection()
        cur = conn.cursor()

        def cargar_dropdown(query, controles):
            cur.execute(query)
            data = [ft.dropdown.Option(str(row[0]), row[1]) for row in cur.fetchall()]
            for c in controles:
                c.options = data.copy()

        cargar_dropdown("SELECT idPerfil, nombre_perfil FROM perfil", [filtro_perfil])
        cargar_dropdown("SELECT idColor, nombre_color FROM color", [filtro_color_alu, filtro_color_cri, filtro_color_her])
        cargar_dropdown("SELECT idSerie, nombre_serie FROM serie", [filtro_serie])
        cargar_dropdown("SELECT idTipo_cristal, nombre_tipo FROM tipo_cristal", [filtro_tipo])
        cargar_dropdown("SELECT idEspesor, medida_mm FROM espesor", [filtro_espesor])
        cargar_dropdown("SELECT idCarretas, nombre_carretas FROM carretas", [filtro_carretas])

        conn.close()

    def cargar_stock_aluminio(e=None):
        tabla_aluminio.rows.clear()
        conn = get_connection(); cur = conn.cursor()

        query = """
            SELECT a.idAluminio, CONCAT(p.nombre_perfil, ' / ', c.nombre_color, ' / ', s.nombre_serie), IFNULL(sa.cantidad, 0)
            FROM aluminio a
            LEFT JOIN perfil p ON a.idPerfil = p.idPerfil
            LEFT JOIN color c ON a.idColor = c.idColor
            LEFT JOIN serie s ON a.idSerie = s.idSerie
            LEFT JOIN stock_aluminio sa ON a.idAluminio = sa.idAluminio
        """
        filtros = []
        valores = []

        if filtro_perfil.value:
            filtros.append("a.idPerfil = %s")
            valores.append(filtro_perfil.value)
        if filtro_color_alu.value:
            filtros.append("a.idColor = %s")
            valores.append(filtro_color_alu.value)
        if filtro_serie.value:
            filtros.append("a.idSerie = %s")
            valores.append(filtro_serie.value)

        if filtros:
            query += " WHERE " + " AND ".join(filtros)

        cur.execute(query, valores)
        for row in cur.fetchall():
            tabla_aluminio.rows.append(ft.DataRow([ft.DataCell(ft.Text(str(col))) for col in row]))
        conn.close(); page.update()

    def cargar_stock_cristal(e=None):
        tabla_cristal.rows.clear()
        conn = get_connection(); cur = conn.cursor()

        query = """
            SELECT c.idCristal, CONCAT(t.nombre_tipo, ' / ', co.nombre_color, ' / ', esp.medida_mm), IFNULL(s.cantidad, 0)
            FROM cristal c
            LEFT JOIN tipo_cristal t ON c.idTipo_cristal = t.idTipo_cristal
            LEFT JOIN color co ON c.idColor = co.idColor
            LEFT JOIN espesor esp ON c.idEspesor = esp.idEspesor
            LEFT JOIN stock_cristal s ON c.idCristal = s.idCristal
        """
        filtros = []
        valores = []

        if filtro_tipo.value:
            filtros.append("c.idTipo_cristal = %s")
            valores.append(filtro_tipo.value)
        if filtro_color_cri.value:
            filtros.append("c.idColor = %s")
            valores.append(filtro_color_cri.value)
        if filtro_espesor.value:
            filtros.append("c.idEspesor = %s")
            valores.append(filtro_espesor.value)

        if filtros:
            query += " WHERE " + " AND ".join(filtros)

        cur.execute(query, valores)
        for row in cur.fetchall():
            tabla_cristal.rows.append(ft.DataRow([ft.DataCell(ft.Text(str(col))) for col in row]))
        conn.close(); page.update()

    def cargar_stock_herrajes(e=None):
        tabla_herrajes.rows.clear()
        conn = get_connection(); cur = conn.cursor()

        query = """
            SELECT h.idHerrajes, CONCAT(ca.nombre_carretas, ' / ', co.nombre_color), IFNULL(s.cantidad, 0)
            FROM herrajes h
            LEFT JOIN carretas ca ON h.idCarretas = ca.idCarretas
            LEFT JOIN color co ON h.idColor = co.idColor
            LEFT JOIN stock_herrajes s ON h.idHerrajes = s.idHerrajes
        """
        filtros = []
        valores = []

        if filtro_carretas.value:
            filtros.append("h.idCarretas = %s")
            valores.append(filtro_carretas.value)
        if filtro_color_her.value:
            filtros.append("h.idColor = %s")
            valores.append(filtro_color_her.value)

        if filtros:
            query += " WHERE " + " AND ".join(filtros)

        cur.execute(query, valores)
        for row in cur.fetchall():
            tabla_herrajes.rows.append(ft.DataRow([ft.DataCell(ft.Text(str(col))) for col in row]))
        conn.close(); page.update()

    def restablecer_filtros():
        for f in [
            filtro_perfil, filtro_color_alu, filtro_serie,
            filtro_tipo, filtro_color_cri, filtro_espesor,
            filtro_carretas, filtro_color_her
        ]:
            f.value = None
        cargar_stock_aluminio()
        cargar_stock_cristal()
        cargar_stock_herrajes()

    cargar_opciones()
    cargar_stock_aluminio()
    cargar_stock_cristal()
    cargar_stock_herrajes()

    return ft.Column([
        ft.ElevatedButton("Restablecer Filtros", on_click=lambda e: restablecer_filtros()),

        ft.Text("Stock de Aluminio", size=18, weight="bold"),
        ft.Row([filtro_perfil, filtro_color_alu, filtro_serie,
                ft.ElevatedButton("Buscar", on_click=cargar_stock_aluminio)], wrap=True),
        ft.Column([tabla_aluminio], height=200, scroll=ft.ScrollMode.ALWAYS),

        ft.Divider(),

        ft.Text("Stock de Vidrio", size=18, weight="bold"),
        ft.Row([filtro_tipo, filtro_color_cri, filtro_espesor,
                ft.ElevatedButton("Buscar", on_click=cargar_stock_cristal)], wrap=True),
        ft.Column([tabla_cristal], height=200, scroll=ft.ScrollMode.ALWAYS),

        ft.Divider(),

        ft.Text("Stock de Herrajes", size=18, weight="bold"),
        ft.Row([filtro_carretas, filtro_color_her,
                ft.ElevatedButton("Buscar", on_click=cargar_stock_herrajes)], wrap=True),
        ft.Column([tabla_herrajes], height=200, scroll=ft.ScrollMode.ALWAYS),
    ])



import flet as ft
from db_connection import get_connection

def aluminio_view(page: ft.Page) -> ft.Control:
    page.title = "Aluminio"
    # Quito el scroll de toda la pagina pa
    # page.scroll = ft.ScrollMode.AUTO

    # ──────────────── CONTROLES ────────────────
    # Filtros de búsqueda
    filtro_perfil = ft.Dropdown(label="Perfil", options=[], width=150)
    filtro_color = ft.Dropdown(label="Color", options=[], width=150)
    filtro_serie = ft.Dropdown(label="Serie", options=[], width=150)

    # Formulario de nuevo registro
    nuevo_perfil = ft.Dropdown(label="Perfil", options=[], width=150)
    nuevo_color = ft.Dropdown(label="Color", options=[], width=150)
    nuevo_serie = ft.Dropdown(label="Serie", options=[], width=150)
    nuevo_largo = ft.TextField(label="Largo", width=150, keyboard_type=ft.KeyboardType.NUMBER)

    # Tabla de resultados
    tabla = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Perfil")),
        ft.DataColumn(ft.Text("Color")),
        ft.DataColumn(ft.Text("Serie")),
        ft.DataColumn(ft.Text("Largo")),
        ft.DataColumn(ft.Text("Acciones")),
    ])

    # ──────────────── FUNCIONES ────────────────
    def cargar_opciones():
        """Carga los valores de los dropdowns desde la base de datos."""
        conn = get_connection()
        cur = conn.cursor()

        def cargar_y_asignar(query, lista):
            cur.execute(query)
            opciones = [ft.dropdown.Option(str(id), nombre) for id, nombre in cur.fetchall()]
            for dd in lista:
                dd.options = opciones.copy()

        cargar_y_asignar("SELECT idPerfil, nombre_perfil FROM perfil", [filtro_perfil, nuevo_perfil])
        cargar_y_asignar("SELECT idColor, nombre_color FROM color", [filtro_color, nuevo_color])
        cargar_y_asignar("SELECT idSerie, nombre_serie FROM serie", [filtro_serie, nuevo_serie])

        conn.close()
        page.update()

    def cargar_registros(e=None):
        """Carga los registros de aluminio en la tabla, aplicando filtros si los hay."""
        tabla.rows.clear()
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT a.idAluminio, p.nombre_perfil, c.nombre_color, s.nombre_serie, a.largo
            FROM aluminio a
            LEFT JOIN perfil p ON a.idPerfil = p.idPerfil
            LEFT JOIN color c ON a.idColor = c.idColor
            LEFT JOIN serie s ON a.idSerie = s.idSerie
        """

        filtros, valores = [], []
        if filtro_perfil.value:
            filtros.append("a.idPerfil = %s")
            valores.append(filtro_perfil.value)
        if filtro_color.value:
            filtros.append("a.idColor = %s")
            valores.append(filtro_color.value)
        if filtro_serie.value:
            filtros.append("a.idSerie = %s")
            valores.append(filtro_serie.value)
        if filtros:
            query += " WHERE " + " AND ".join(filtros)

        cur.execute(query, valores)
        for id_, perfil, color, serie, largo in cur.fetchall():
            tabla.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(id_))),
                ft.DataCell(ft.Text(perfil or "")),
                ft.DataCell(ft.Text(color or "")),
                ft.DataCell(ft.Text(serie or "")),
                ft.DataCell(ft.Text(str(largo))),
                ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=id_: eliminar(id)))
            ]))

        conn.close()
        page.update()

    def agregar_registro(e):
        """Agrega un nuevo registro a la tabla de aluminio."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COALESCE(MAX(idAluminio), 0) + 1 FROM aluminio")
        nuevo_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO aluminio (idAluminio, idPerfil, idColor, idSerie, largo)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            nuevo_id,
            int(nuevo_perfil.value),
            int(nuevo_color.value),
            int(nuevo_serie.value),
            float(nuevo_largo.value)
        ))
        conn.commit()
        conn.close()
        cargar_registros()

    def eliminar(id):
        """Elimina un registro por ID."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM aluminio WHERE idAluminio = %s", (id,))
        conn.commit()
        conn.close()
        cargar_registros()

    def limpiar_filtros(e):
        filtro_perfil.value = filtro_color.value = filtro_serie.value = None
        cargar_registros()

    # ──────────────── DISEÑO DE LA PANTALLA ────────────────
    cargar_opciones()
    cargar_registros()

    return ft.Column([
        ft.Text("Filtros", size=16, weight="bold"),
        ft.Row([filtro_perfil, filtro_color, filtro_serie, ft.ElevatedButton("Buscar", on_click=cargar_registros), ft.ElevatedButton("Limpiar", on_click=limpiar_filtros)], spacing=10),
        ft.Divider(),
        ft.Text("Agregar Nuevo", size=16, weight="bold"),
        ft.Row([nuevo_perfil, nuevo_color, nuevo_serie, nuevo_largo, ft.ElevatedButton("Agregar", on_click=agregar_registro)], spacing=10),
        ft.Divider(),
        ft.Text("Registros", size=16, weight="bold"),
        # Envolvemos la tabla en un Column con scroll y altura fija
        ft.Container(
            content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
            height=400,  # Altura fija para la tabla
            padding=10
        )
    ])

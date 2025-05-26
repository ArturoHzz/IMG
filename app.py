import flet as ft
from crud_aluminio import aluminio_view
from crud_vidrio import vidrio_view
from crud_herrajes import herrajes_view
from crud_compra import compra_view
from crud_venta import venta_view
from stock_view import stock_view

def main(page: ft.Page):
    page.title = "Gestión de Inventario"

    # Encabezado visual
    encabezado = ft.Container(
        content=ft.Text("Sistema de Gestión de Inventario", size=24, weight="bold"),
        alignment=ft.alignment.center,
        padding=20
    )

    # Pestañas
    pestañas = ft.Tabs(tabs=[
        ft.Tab(text="Aluminio", content=aluminio_view(page)),
        ft.Tab(text="Vidrio", content=vidrio_view(page)),
        ft.Tab(text="Herrajes", content=herrajes_view(page)),
        ft.Tab(text="Compras", content=compra_view(page)),
        ft.Tab(text="Ventas", content=venta_view(page)),
        ft.Tab(text="Stock", content=stock_view(page)),
    ], expand=1)

    page.add(encabezado, pestañas)

if __name__ == "__main__":
    ft.app(target=main)



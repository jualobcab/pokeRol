import flet as ft
import sqlite3 as sql

pokemon_list_cache = None
POKEMONS = []


def load_pokemons():
    conn = sql.connect("pokeRol.db")
    cursor = conn.cursor()

    cursor.execute("SELECT ID, DEX_NUM, NAME FROM POKEMONS")
    items = cursor.fetchall()

    conn.close()
    return items


def get_pokemon(id):
    conn = sql.connect("pokeRol.db")
    cursor = conn.cursor()
    query = """
    SELECT P.DEX_NUM, P.NAME 
    FROM POKEMONS P 
    WHERE P.ID=?
    """

    cursor.execute(query, (id,))
    items = cursor.fetchone()

    conn.close()
    return items


def main(page: ft.Page):
    global POKEMONS
    POKEMONS = load_pokemons()
    page.title = "PokeRPGdex"
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.AMBER,
    )
    page.on_route_change = lambda route: route_change(page, route)
    page.go("/")  # ruta inicial


def route_change(page: ft.Page, route: str):
    page.views.clear()

    if page.route == "/":
        page.views.append(
            ft.View(
                "/",
                controls=[get_list_view(page)]
            )
        )

    elif page.route.startswith("/detail/"):
        pokemon_id = int(page.route.split("/")[-1])
        page.views.append(
            ft.View(
                f"/detail/{pokemon_id}",
                controls=[get_detail_view(page, pokemon_id)]
            )
        )

    page.update()


def create_card(_id, dex_num, name):
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row(
                    [
                        ft.Text(f"#{str(dex_num).zfill(4)}")
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
                ft.Image(src=f"images/PokemonSprites/{_id}.png", width=100, height=100,
                         fit=ft.ImageFit.CONTAIN),
                ft.Text(name)
            ],
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=10,
            width=None,  # None = se ajusta al contenido
            height=None
        ),
        elevation=3,
        margin=10
    )


def get_list_view(page):
    global pokemon_list_cache

    if pokemon_list_cache is None:
        cards = []

        for _id, dex_num, name in POKEMONS:
            cards.append(
                ft.GestureDetector(
                    content=create_card(_id, dex_num, name),
                    on_tap=lambda e, id=_id: page.go(f"/detail/{id}")
                )
            )

        pokemon_list_cache = ft.GridView(
            controls=cards,
            expand=True,
            max_extent=215,
            child_aspect_ratio=0.9,
            spacing=10,
            run_spacing=10
        )

    return pokemon_list_cache


def get_detail_view(page, pokemon_id):
    dex_num, name = get_pokemon(pokemon_id)

    return ft.Column(
        [
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Volver",
                        on_click=lambda e: page.go("/")
                    ),
                    ft.Text(f"#{dex_num:04d}")
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Text(name, size=20, weight=ft.FontWeight.BOLD),
            ft.Image(
                src=f"images/PokemonSprites/{pokemon_id}.png",
                width=200,
                height=200,
                fit=ft.ImageFit.CONTAIN
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )


ft.app(main)

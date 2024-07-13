# -*- coding: utf-8 -*-
import dash
from dash import Dash, html, dcc
import dash_leaflet as dl
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import os
from dash_extensions.javascript import assign, arrow_function
import geopandas as gpd
import json
import random
## Poligonos
# Leer el archivo GeoJSON con GeoPandas
directorio_actual = os.getcwd()
ruta_archivo = os.path.join(directorio_actual, "assets", "brown1.geojson")

gdf = gpd.read_file(ruta_archivo)
# Convertir el GeoDataFrame a GeoJSON estándar
geojson_data = json.loads(gdf.to_json())

# Función para generar colores aleatorios
def random_color():
    """
    Genera un color hexadecimal aleatorio.
    """
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color

# Asignar colores aleatorios a cada polígono en el GeoJSON
for feature in geojson_data['features']:
    feature['properties']['style'] = {
        'color': random_color(),
        'weight': 3
    }

# Función JavaScript para el estilo de hover
hover_style = arrow_function(dict(weight=5, color='#5F9EA0', dashArray=''))


# Lista para almacenar los componentes dl.GeoJSON
geojson_layers = []

# Crear un componente dl.GeoJSON para cada polígono
for feature in geojson_data['features']:
    if feature['geometry']['type'] in ['Polygon', 'MultiPolygon']:
        geojson_layers.append(
            dl.GeoJSON(
            id=f"geojson_{feature['properties']['id']}",  # ID único para cada polígono (puedes ajustar esto según tus necesidades)
            data=feature,
            options=dict(style=feature['properties']['style']),
            hoverStyle=hover_style
        )
    )
###


button_on_click = assign("""
function(btn, map) {
    if (!btn.button.options) btn.button.options = {};
    if (btn.button.options.state === 'white') {
        btn.button.style.setProperty('background-color', 'aqua', 'important');  // Cambiar a blanco con !important
        btn.button.options.state = 'aqua';  // Actualizar estado
    } else {
        btn.button.style.setProperty('background-color', 'white', 'important');  // Cambiar a azul con !important
        btn.button.options.state = 'white';  // Actualizar estado
    }
}
""")

directorio_actual = os.getcwd()
ruta_archivo = os.path.join(directorio_actual, "assets", "puntos_interes.xlsx")
df = pd.read_excel(ruta_archivo)
icon_reciclaje = dict(
    iconUrl='/assets/recycling_189286.png',
    iconSize=[32, 32],
    iconAnchor=[16, 32]
)
icon_recoleccion = dict(
    iconUrl='/assets/garbage-truck_8766985.png',
    iconSize=[32, 32],
    iconAnchor=[16, 32]
)
icon_mascotas = dict(
    iconUrl='/assets/pet-friendly_12141154.png',
    iconSize=[32, 32],
    iconAnchor=[16, 32]
)
BROWN_LOGO = "/assets/LOGO-01A.png"
INFO_LOGO = "/assets/information.png"
STYLE_OFF = {
    "background-color": "#0f6cbf",
    "color": "white"
}

map_layers = [
    {
        "id": "streets",
        "name": "Streets",
        "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "maxZoom": 19,
        "attribution": "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors"
    },
    {
        "id": "dark",
        "name": "Dark",
        "url": "http://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
        "maxZoom": 19,
        "attribution": "Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ"
    },
    {
        "id": "satellite",
        "name": "Satellite",
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "maxZoom": 19,
        "attribution": "Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ"
    },
    {
        "id": "sdse",
        "name": "Hibridro",
        "url": "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        "maxZoom": 19,
        "attribution": "Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ"
    },
    {
        "id": "topo",
        "name": "Topo",
        "url": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        "maxZoom": 17,
        "attribution": "Map data: &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors, <a href=\"http://viewfinderpanoramas.org\">SRTM</a> | Map style: &copy; <a href=\"https://opentopomap.org\">OpenTopoMap</a> (<a href=\"https://creativecommons.org/licenses/by-sa/3.0/\">CC-BY-SA</a>)"
    }
]

modal = dbc.Modal([
    dbc.ModalHeader("Ayuda"),
    dbc.ModalBody(
        dbc.Card([
            dbc.CardBody([
                html.P("Utiliza el control de capas en la esquina superior derecha para cambiar entre diferentes capas de mapa (Streets, Dark, Satellite, Hibridro, Topo)."),
                html.P("Haz clic en los botones en la esquina izquierda para mostrar u ocultar diferentes tipos de puntos de interés: Centros de Reciclaje, Recoleccion de Residuos, Cuidado animal."),
                html.P("Los marcadores en el mapa muestran información adicional al pasar el cursor sobre ellos"),
                html.P("Al hacer click en los marcadores nos da información especifica de los puntos de interes"),
            ])
        ])
    ),
    dbc.ModalFooter(
        dbc.Button("Cerrar", id="close-help-modal", className="ml-auto")
    ),
], id="help-modal", size="xl", scrollable=True)

# Añadir CSS para el ícono.
external_css = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"

# Crear la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, external_css])

# Crear el layout de la aplicación
app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=BROWN_LOGO, height="50px")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://www.almirantebrown.gov.ar/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarBrand("Mapa Interactivo", className="ms-2 center"),
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=INFO_LOGO, height="34px")),
                    ],
                    align="center",
                    className="g-0",
                ),
                id="open-help-modal",  # ID para abrir el modal
                style={"cursor": "pointer", "textDecoration": "none"},
            ),
        ], style={"height": "50px", "margin": "0", "padding": "0"}),
        color="#0f6cbf",
        dark=True,
        className="mb-0",
    ),

    dl.Map(
        id="map",
        style={'width': '100%', 'height': '75vh', "margin": "0", "padding": "0"},
        center=[-34.80, -58.38],
        zoom=12,
        children=[
            dl.TileLayer(),
            dl.LayerGroup(id="layer"),
            *geojson_layers,  # Desempaquetar la lista de componentes dl.GeoJSON
            dl.LayersControl(
                [
                    dl.BaseLayer(
                        dl.TileLayer(
                            url=layer["url"],
                            attribution=layer["attribution"],
                            maxZoom=layer.get("maxZoom", 18),
                            subdomains=layer.get("subdomains", "abc"),
                            bounds=layer.get("bounds", None)
                        ),
                        name=layer["name"],
                        checked=(layer["id"] == "streets")  # Seleccionar por defecto
                    )
                    for layer in map_layers
                ],
                id="layers_control"
            ),
            dl.EasyButton(icon="fa fa-recycle", title="Centros de Reciclaje", id="btn1", n_clicks=0, eventHandlers={'click': button_on_click}),
            dl.EasyButton(icon="fa fa-truck", title="Recoleccion de Residuos", id="btn2", n_clicks=0, eventHandlers={'click': button_on_click}),
            dl.EasyButton(icon="fa fa-paw", title="Cuidado Animal", id="btn3", n_clicks=0, eventHandlers={'click': button_on_click})
        ]
    ),
    dbc.Offcanvas(
        id="sidebar",
        title="Detalles del Punto",
        is_open=False,
        children=[
            html.H5(id="sidebar-title"),
            html.P(id="sidebar-description"),
            html.P(id="sidebar-direccion"),
            html.P(id="sidebar-telefono"),
            html.P(id="sidebar-localidad")
        ],
        style=STYLE_OFF
    ),
    modal,
    dbc.Container(
        dbc.Row(
            dbc.Col(

                    dbc.CardBody(
                        [
                            html.H4("Seguinos"),
                            html.A(
                                html.I(className="fa fa-facebook"),
                                href="https://www.facebook.com",
                                style={"margin-right": "10px","color":"white","padding":"5px"}
                            ),
                            html.A(
                                html.I(className="fa fa-twitter"),
                                href="https://www.twitter.com",
                                style={"margin-right": "10px","color":"white","padding":"5px"}
                            ),
                            html.A(
                                html.I(className="fa fa-instagram"),
                                href="https://www.instagram.com",
                                style={"margin-right": "10px","color":"white","padding":"5px"}
                            ),
                            html.A(
                                html.I(className="fa fa-linkedin"),
                                href="https://www.linkedin.com",
                                style={"margin-right": "10px","color":"white","padding":"5px"}
                            )
                        ],
                        className="d-flex justify-content-center align-items-center",
                        style={"background-color": "#0f6cbf", "color": "white"}
                    ),
                    className="mt-4"


            )
        )
    )
], style={"margin": "0", "padding": "0", "overflow": "hidden"})


@app.callback(
    [Output("help-modal", "is_open")],
    [Input("open-help-modal", "n_clicks"), Input("close-help-modal", "n_clicks")],
    [State("help-modal", "is_open")],
    prevent_initial_call=True,
)
def toggle_help_modal(open_clicks, close_clicks, is_open):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "open-help-modal":
            return [True]
        elif button_id == "close-help-modal":
            return [False]
    return [is_open]


@app.callback(Output("layer", "children"), Input("btn1", "n_clicks"), Input("btn2", "n_clicks"), Input("btn3", "n_clicks"))
def updates_markers(btn1_clicks, btn2_clicks, btn3_clicks):
    click1 = int(btn1_clicks)
    click2 = int(btn2_clicks)
    click3 = int(btn3_clicks)
    show_markers = (click1 % 2 == 0) or (click2 % 2 == 0) or (click3 % 2 == 0)  # Mostrar marcadores si algún botón está en estado 'aqua'
    if show_markers:
        active_types = []
        if btn1_clicks % 2 == 0:
            active_types.append('reciclaje')
        if btn2_clicks % 2 == 0:
            active_types.append('recoleccion')
        if btn3_clicks % 2 == 0:
            active_types.append('cuidado_animal')

        markers = []

        for i, row in df.iterrows():
            if row['tipo'] in active_types:
                if row["tipo"] == "reciclaje":
                    icon_type = icon_reciclaje
                elif row["tipo"] == "recoleccion":
                    icon_type = icon_recoleccion
                elif row["tipo"] == "cuidado_animal":
                    icon_type = icon_mascotas
                markers.append(dl.Marker(position=[row['latitud'], row['longitud']], icon=icon_type, id={"type": "marker", "index": i}, children=dl.Tooltip(row['nombre'])))
        return markers


@app.callback(
    [
        Output("sidebar", "is_open"),
        Output("sidebar-title", "children"),
        Output("sidebar-description", "children"),
        Output("sidebar-direccion", "children"),
        Output("sidebar-telefono", "children"),
        Output("sidebar-localidad", "children")
    ],
    [Input({"type": "marker", "index": dash.dependencies.ALL}, "n_clicks")],
    [State("layer", "children")]
)
def display_info(n_clicks, markers):
    ctx = dash.callback_context
    if not ctx.triggered or all(click is None for click in n_clicks):
        return False, "", "", "", "", ""

    marker_id = ctx.triggered[0]["prop_id"].split(".")[0]
    index = int(eval(marker_id)["index"])
    selected_row = df.iloc[index]
    if pd.isna(selected_row["telefono"]):
        telefono = "Sin Especificar"
    else:
        telefono = selected_row["telefono"]
    return (
        True,
        selected_row["nombre"],
        selected_row["descripcion"],
        f"Dirección: {selected_row['direccion']}",
        f"Teléfono: {telefono}",
        f"Localidad: {selected_row['localidad']}"
    )


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)

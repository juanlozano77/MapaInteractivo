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
ruta_archivo = os.path.join(directorio_actual, "assets", "brown.geojson")

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

print (geojson_layers)
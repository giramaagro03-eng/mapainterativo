import geopandas as gpd
import folium

# 1. Carregar todas as camadas
grid = gpd.read_file('grid_2kmX2km.shp').to_crs(epsg=4326)
poligonos_fauna = gpd.read_file('Poligono_ESPECIES_anfibios.shp').to_crs(epsg=4326)
pontos_fauna = gpd.read_file('lista_ESPECIES_anfibios.shp').to_crs(epsg=4326)

# Se tiveres a camada do limite da Paraíba/Brasil dentro de base_BR:
# paraiba = gpd.read_file('base_BR/PB_Limite.shp').to_crs(epsg=4326)

# 2. Centrar o mapa na área de estudo (Paraíba)
centro_lat = grid.geometry.centroid.y.mean()
centro_lon = grid.geometry.centroid.x.mean()

mapa = folium.Map(
    location=[centro_lat, centro_lon],
    zoom_start=8,
    tiles='OpenStreetMap'
)

# Adicionar mapa base de Imagem de Satélite
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Imagem de Satélite (Esri)',
    overlay=False
).add_to(mapa)

# 3. Adicionar Camada 1: Polígonos das Espécies (Área de distribuição)
folium.GeoJson(
    poligonos_fauna,
    name='Polígonos de Distribuição (Fauna)',
    style_function=lambda x: {
        'fillColor': '#ff7800',
        'color': '#ff7800',
        'weight': 2,
        'fillOpacity': 0.3
    },
    tooltip=folium.GeoJsonTooltip(fields=list(poligonos_fauna.columns.drop('geometry')))
).add_to(mapa)

# 4. Adicionar Camada 2: Grid 2km x 2km
folium.GeoJson(
    grid,
    name='Grid de Amostragem (2km x 2km)',
    style_function=lambda x: {
        'fillColor': '#3186cc',
        'color': '#000000',
        'weight': 1,
        'fillOpacity': 0.15
    },
    tooltip=folium.GeoJsonTooltip(fields=['id', 'row_index', 'col_index'], aliases=['ID:', 'Linha:', 'Coluna:'])
).add_to(mapa)

# 5. Adicionar Camada 3: Pontos de Ocorrência da Fauna
# Se for camada de pontos
folium.GeoJson(
    pontos_fauna,
    name='Pontos de Fauna / Ocorrências',
    marker=folium.CircleMarker(radius=4, color='red', fill=True, fill_color='red'),
    tooltip=folium.GeoJsonTooltip(fields=list(pontos_fauna.columns.drop('geometry')))
).add_to(mapa)

# 6. Adicionar Controle de Camadas (Permite ligar/desligar cada camada no canto superior direito)
folium.LayerControl(collapsed=False).add_to(mapa)

# 7. Salvar o mapa interativo
mapa.save('index.html')
print("Mapa completo gerado com sucesso!")

import geopandas as gpd
import folium

# 1. Carregar o arquivo espacial do grid
# Substitua 'seu_arquivo.shp' pelo nome correto do seu arquivo no repositório
caminho_arquivo = 'seu_arquivo.shp' 
gdf = gpd.read_file(caminho_arquivo)

# 2. Garantir coordenadas WGS 84 (EPSG:4326) para visualização web
if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
    gdf = gdf.to_crs(epsg=4326)

# 3. Calcular o centro do mapa
centro_lat = gdf.geometry.centroid.y.mean()
centro_lon = gdf.geometry.centroid.x.mean()

# 4. Criar o mapa base
mapa = folium.Map(
    location=[centro_lat, centro_lon],
    zoom_start=12,
    tiles='OpenStreetMap'
)

# Adicionar mapa base com imagem de satélite (Esri)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Imagem de Satélite (Esri)',
    overlay=False,
    control=True
).add_to(mapa)

# 5. Adicionar a camada do Grid ao mapa
folium.GeoJson(
    gdf,
    name='Grid de Estudo',
    style_function=lambda feature: {
        'fillColor': '#3186cc',
        'color': '#000000',      # Cor da borda
        'weight': 1,            # Espessura da borda
        'fillOpacity': 0.2,     # Transparência do preenchimento
    },
    highlight_function=lambda feature: {
        'weight': 3,
        'color': '#ff0000',
        'fillOpacity': 0.5,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['id', 'row_index', 'col_index'],  # Nomes das colunas da tabela do seu grid
        aliases=['ID:', 'Linha:', 'Coluna:'],
        localize=True
    )
).add_to(mapa)

# 6. Adicionar controle de camadas
folium.LayerControl().add_to(mapa)

# 7. Salvar o mapa interativo em HTML
mapa.save('index.html')

print("Mapa interativo gerado com sucesso!")

import geopandas as gpd
import re
from shapely import wkt
import folium
import streamlit as st
import streamlit_folium

try:
    uploaded_file = st.file_uploader("Please Upload GeoJSON or ZIP Shapefiles here")
    geofence_gdf = gpd.read_file(uploaded_file)
    geofence_gdf['str_geom'] = geofence_gdf.geometry.apply(lambda x: wkt.dumps(x))
    
    # CONVERT QGIS GEOMETRY TO GEOTOOLS COORDINATES
    for i, row in geofence_gdf.iterrows():
       # EXTRACTING THE COORDINATES FROM STR GEOM USING REGEX
       coordinates_match = re.search(r'POLYGON \(\((.*?)\)\)', row['str_geom'])
    if coordinates_match:
        coordinates_text = coordinates_match.group(1)
        coordinates = coordinates_text.split(', ')

          #REFORMATING THE COORDINATES ACCORDING GEOTOOLS
        reformatted_coordinates = []
        for coord in coordinates:
            x,y = coord.split(' ')
            reformatted_coordinates.append(f'{y}, {x}')

        #JOINING THE REFORMATTED COORDINATES WITH COMMAS
            result_string = ', '.join(reformatted_coordinates)
            geofence_gdf.at[i, 'geotools_coordinates'] = result_string
        else:
            st.write("invalid input string")
    
       
    output = st.text_input('File Save As', )
    csv=geofence_gdf.to_csv()
    st.download_button(
      label="Download data as CSV",
      data=csv,
      file_name = output+'.csv',
      mime='text/csv',
  )

except (TypeError, NameError, AttributeError):
  pass
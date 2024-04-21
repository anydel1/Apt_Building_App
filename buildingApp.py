import os
import streamlit as st
from topologicpy.Vertex import Vertex
from topologicpy.CellComplex import CellComplex
from topologicpy.Cluster import Cluster
from topologicpy.Graph import Graph
from topologicpy.Plotly import Plotly
from topologicpy.Neo4j import Neo4j
from storeys import create_building
from roof import create_roof
from face_dictionaries import create_face_dictionaries

#### building Parameters
origin = Vertex.ByCoordinates(0, 0, 0)
bPlacement = 'lowerleft'

# diagram mode selection
display_option = st.sidebar.selectbox(
    'Select an option', ('Show building', 'Show graph', 'Show building and graph'))

# Create sliders for the parameters
bLength = st.sidebar.slider('Length', min_value=10, max_value=40, value=22)
bWidth = st.sidebar.slider('Width', min_value=10, max_value=30, value=16)
storeyHeight = st.sidebar.slider('Storey Height', min_value=1, max_value=10, value=3)
storeys = st.sidebar.slider('Number of Storeys', min_value=1, max_value=12, value=6)
storey_1_height = st.sidebar.slider('First Storey Height', min_value=1, max_value=10, value=4)
ridge_height = st.sidebar.slider('Ridge Height', min_value=1, max_value=10, value=4)
ridge_length = st.sidebar.slider('Ridge Length', min_value=1, max_value=bLength, value=10)


#call
building, selectors, topFace, vertices, stHeight = create_building(origin, bWidth, bLength, bPlacement, storeyHeight, storey_1_height, storeys)

# call
roof, selectors, stHeight = create_roof(topFace, bWidth, selectors, stHeight, ridge_height, ridge_length)

building = Cluster.ByTopologies(building, roof)
building = CellComplex.ByCellsCluster(building)


if __name__ == '__main__':    
    # CALL create_face_dictionaries
    topologies, vertexGroups = create_face_dictionaries(building, selectors)
    
    graph = Graph.ByTopology(building, toExteriorTopologies=True, viaSharedTopologies=True, storeBRep=False)

    data01 = Plotly.DataByGraph(graph, vertexGroupKey="group", vertexLabelKey="type", vertexGroups=vertexGroups, colorScale="turbo")
    data02 = Plotly.DataByTopology(building, showVertices=True, edgeWidth=2, edgeColor="white", vertexSize= 3.0, vertexColor="red", faceOpacity=0.5)
    
    # Combine the building data and graph into a single Plotly figure.
    combined_data = data01 + data02
    figure = Plotly.FigureByData(combined_data, width=950, height=600, backgroundColor="white", marginTop=5) # backgroundColor="rgb(14, 17, 23)") for dark mode.
    figure = Plotly.SetCamera(figure, camera=[2.00, 1.85, 0.35], center=[0, 0, 0], up=[0, 0, 1], projection="perspective")


    # Connect to Neo4j database
    
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = os.getenv('NEO4J_PASSWORD')
    
    
    neoGraph = Neo4j.ByParameters(uri, user, password)
    neoGraph = Neo4j.DeleteAll(neoGraph)
    # Add Topologic graph to Neo4j database
    Neo4j.SetGraph(neoGraph, graph, labelKey='group', relationshipKey='IS_PART_OF')
    # nodeLabels = Neo4j.NodeLabels(neoGraph)
    # print(nodeLabels)

    # Show plotly figure based on the user's selection
    if display_option == 'Show building':
        figure.data = [data for data in figure.data if 'Topology' in data.name]
    elif display_option == 'Show graph':
        figure.data = [data for data in figure.data if 'Graph' in data.name]
        
    # Show plotly figure based on the user's selection
    if display_option == 'Hip Roof':
        figure.data = [data for data in figure.data if 'Hip Roof' in data.name]
    elif display_option == 'Gable Roof':
        figure.data = [data for data in figure.data if 'Gable Roof' in data.name]

    # Show plotly figure
    st.plotly_chart(figure, use_container_width=True)

    
  
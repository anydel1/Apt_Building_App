# A Topologic Apartment Building App

This simple web application demonstrates the use of **Topologicpy** to create a topological/graph-based apartment building with some basic parametric features. It integrates with a **Neo4j graph database** for the creation, storage, and real-time updating of building data. The user interface is powered by **Streamlit** for quick development feedback.

## Parametric Modeling Features

The parametric modeling features include:

1. **Dropdown Menu**: Choose from the following diagram modes:
    - 'Show Building'
    - 'Show Graph'
    - 'Show Building and Graph'

2. **Sliders**: Adjust the geometry of the building:
    - Overall length and width
    - Storey heights (including independently changing the first storey height)
    - Number of storeys
    - Roof ridge height and length

## Neo4j Database Connection

The Neo4j database connection automatically creates a property graph of the building, and dynamically updates changes made by the user in the web application, adding new nodes and relationships for new apartments created when adding additional storeys. It also updates the apartment numbers to include the added apartments in the numbering system.

## Ontologies

The properties of the building elements are stored in the graph nodes and conform to a simplified IFC schema while mapping to the Topologicpy and conventional naming ontologies.

### IFC Ontology

- IfcSpace
- IfcWall
- IfcSlab 
- IfcRoof

### Topologicpy Ontology

- Cell
- External Vertical Face
- Internal Vertical Face
- External Horizontal Face
- Internal Horizontal Face
- External Inclined Face

### Conventional Ontology

- Apartment
- Corridor
- Stairwell
- Attic
- Wall
- Slab
- Roof

At the moment, the graph's relationships are all defined generically as 'connected_to'.

## Future Plans

This was a basic learning exercise to develop a deeper understanding of Topologicpy's modeling and dictionary methods, and translate those into a working application. But it's only the tip of the iceberg. Topologicpy and Neo4j offer much more than modeling and storage. They are also powerful analytic tools, and I plan to tap into those capabilities as I continue.

I'm particularly interested in developing interoperable workflows that leverage the power of graphs to understand the complex relationships in our built environment. I see graphs as the underlying infrastructure that will allow us to seamlessly communicate across different domains, discovering new insights and a deeper understanding of our built environment.

## Acknowledgements

- Topologic is a powerful graph/topology-based software modeling and analysis library developed by Wassim Jabi. Thank you, Wassim! https://github.com/wassimj/topologicpy.git
- Neo4j is a graph database management system to store, analyze, and visualize connected data.
- Streamlit is an open-source Python library that allows you to quickly create and share interactive web applications.

All three support machine learning and AI integration.

Feedback is welcome!

## Tags

#architecture #AEC #topologicpy #neo4j #computationaldesign #openbim  #IFC #buildingSMART #graphtheory

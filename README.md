A simple web application (my first) demonstrating the use of Topologicpy to create a graph-based apartment building with some parametric features and connection to a Neo4j graph database for creating, storing, and updating the building data.

Parametric modeling features include a dropdown menu to choose the diagram mode: 'Show Building', 'Show Graph', 'Show Building and Graph', and sliders to change the geometry of the building. With the sliders you can change the overall length and width of the building, the storey heights - including independently changing the first storey height, the number of storeys, and the roof ridge height and length.

The application connects to a Neo4j database automatically creating a property graph version of the building. The database dynamically updates to conform to the parametric changes made in the web application. This includes adding new nodes and relationships for the new apartments created when adding additional storeys, as well as dynamically updating the apartment numbers to include the added apartments in the numbering system.

The properties of the nodes conform to a simplifed IFC schema while mapping to topologicpy and conventional naming ontologies.

  IFC Ontology: 
  IfcSpace, 
  IfcWall, 
  IfcSlab, 
  IfcRoof, 
  
  Topologicpy Ontology: 
  Cell, 
  External Vertical Face, 
  Internal Vertical Face, 
  External Horizontal Face, 
  Internal Horizontal Face, 
  External Inclined Face, 
  
  Conventional Ontology: 
  Apartment, 
  Cooridor, 
  Stairwell, 
  Attic, 
  Wall, 
  Floor_Slab, 
  Roof, 

The Graph's relationships are all defined generically as 'connected_to'
	

from topologicpy.Vertex import Vertex
from topologicpy.Face import Face
from topologicpy.Cell import Cell
from topologicpy.CellComplex import CellComplex
from topologicpy.Cluster import Cluster
from topologicpy.Topology import Topology
from topologicpy.Dictionary import Dictionary

# number of units Parameter
n_units = 2

#### building Parameters
origin = Vertex.ByCoordinates(0, 0, 0)
bWidth = 15
bLength = 22
bPlacement = 'lowerleft'
storeyHeight = 3
storey_1_height = 4
storeys = 6
ridge_height = 6
baseCorr_origin = origin
cWidth = 2.5
cLength = bWidth
coreWidth = 5
coreLength = 6


def create_building(origin, bWidth, bLength, bPlacement, storeyHeight, storey_1_height, storeys,):
    
#### Initialize total height
    total_height = 0

    # Initialize the list to hold all units and selectors
    units = []
    selectors = []

    for i in range(storeys):
        # Use custom height for the first storey if provided
        if i == 0 and storey_1_height is not None:
            stHeight = storey_1_height
        else:
            stHeight = storeyHeight
        # Add the height of the current storey to the total height
        total_height += stHeight
        # Translate units for each storey
        origin = Vertex.ByCoordinates(0, 0, sum([storey_1_height if j == 0 and storey_1_height is not None else storeyHeight for j in range(i)]))
        complex = CellComplex.Box(origin, width=bWidth, length=bLength, height=stHeight, uSides=1, vSides=n_units, wSides=1, placement=bPlacement)
        cells = CellComplex.Cells(complex)
        cells.sort(key=lambda cell: Vertex.Z(Topology.Centroid(cell)))  # Sort the cells by the Z-coordinate of their centroid
    
        for cell in cells:
            # Get the centroid of the cell
            cen = Topology.Centroid(cell)
            # Get the Z-coordinate of the centroid
            z = Vertex.Z(cen)
            # Determine the storey based on the Z-coordinate
            storey = int(z / storeyHeight) + 1
            # Calculate the unique ID for the unit
            id = storey * 100 + (cells.index(cell) % n_units + 1)
            # Create dictionary     
            d1 = Dictionary.ByKeysValues(["id","group", "entity", "spaceID", "type", "area", "height", "volume"], ["Cells"+str(i), "Cells", "ifcSpace", str(id), "apartment", 30, stHeight, 90])
            t = Topology.SetDictionary(cen, d1)
            selectors.append(cen)
        units.append(complex)
        
    unitsCluster = Cluster.ByTopologies(units)
    cells = Cluster.Cells(unitsCluster)
    basicUnits = CellComplex.ByCells(cells)

    baseCorridor = Cell.Box(baseCorr_origin, bWidth, cWidth, storey_1_height, placement=bPlacement)
    corridorLocated = Topology.Translate(baseCorridor, 0, (bLength/2) - 1.25, 0)
    baseStair = Cell.Box(baseCorr_origin, coreLength, coreWidth, total_height, placement=bPlacement)
    stairLocated = Topology.Translate(baseStair, 0, (bLength/2)-2.5, 0) # moves basecStair to location

    cen = Topology.Centroid(stairLocated) # Find centroid
    # Create dictionary     
    d2 = Dictionary.ByKeysValues(["id","group", "entity", "spaceID", "type", "area", "height", "volume"], ["Cells"+str(i), "Cells", "ifcSpace", "S100", "stairwell", 30, stHeight, 90])
    cen = Topology.SetDictionary(cen, d2)
    selectors.append(cen)

    # Boolean between corridor and stair, create dictionary for corridor.
    corridor = Topology.Boolean(corridorLocated, stairLocated, 'difference')
    cen = Topology.Centroid(corridor)
   
    # Create dictionary     
    d3 = Dictionary.ByKeysValues(["id","group", "entity", "spaceID", "type", "area", "height", "volume"], ["Cells"+str(i), "Cells", "ifcSpace", "C100", "corridor", 30, stHeight, 90])
    cen = Topology.SetDictionary(cen, d3)
    selectors.append(cen)
    
    # combine core and corridor
    core = CellComplex.ByCells([stairLocated, corridor])

    # Boolean operations between the units and the core(stairwell, corridor)
    boolUnitCore = Topology.Boolean(basicUnits, core, 'difference') # difference core/corridor from basic units.
    unitCells = CellComplex.Cells(boolUnitCore) # returns the cells of the units as objects
    unitCells.append(corridor)
    unitCells.append(stairLocated) 
  
    # Sort the cells again by the Z-coordinate of their centroid
    unitCells.sort(key=lambda cell: Vertex.Z(Topology.Centroid(cell)))
    
    # maybe modularize building into a function. Think of reasons why that would be good.
    building = Cluster.ByTopologies(unitCells)
    building = CellComplex.ByCellsCluster(building)

    boundingBox = Topology.BoundingBox(building)
    # get the 'topHorizontalFaces' of the bounding box
    dict = Cell.Decompose(boundingBox)
    topFace = dict['topHorizontalFaces'][0]
    vertices = Face.Vertices(topFace)
    
    
    return(building, selectors, topFace, vertices, stHeight)

# #call
# building, selectors, topFace, vertices = create_building(origin, bWidth, bLength, bPlacement, storeyHeight, storey_1_height, storeys)

# Topology.Show(building, selectors, vertexColor='red', vertexSize=3, renderer="browser")
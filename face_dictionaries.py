from topologicpy.Vertex import Vertex
from topologicpy.CellComplex import CellComplex
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

# #call
# building, selectors = create_building(origin, bWidth, bLength, bPlacement, storeyHeight, storey_1_height, storeys)

def create_face_dictionaries(building, selectors):
    
    # Face variables
    slabEntity = "ifcSlab"
    slabtype1 = "floor_slab"
    slabtype2 = "roof"
    wallEntity = "ifcWall"
    roofEntity = "ifcRoof"
    walltype = "wall"
    area = 30
    height = 3
    
    # Transfer the dictionaries from the selectors to the cells of the CellComplex
    building = Topology.TransferDictionariesBySelectors(building, selectors, tranCells=True, numWorkers=1)

    # Decompose the CellComplex: Returns dictionary of Keys with face groups.
    d = CellComplex.Decompose(building)
    # d['Cells'] = Topology.Cells(building)
    keys = Dictionary.Keys(d)
    # cells = d['Cells']
    externalFaces = d['externalVerticalFaces']
    internalFaces = d['internalVerticalFaces']
    topFaces = d['topHorizontalFaces']
    bottomFaces = d['bottomHorizontalFaces']
    internalHorizFaces = d['internalHorizontalFaces']
    externalInclinedFaces = d['externalInclinedFaces']
    # Create list of vertexGoups culling unused groups.
    vertexGroups = []
    for key in keys:
        topologies = d[key]
        if len(topologies) > 0:
            vertexGroups.append(key)
    # Assign Dictionaries to objects in face groups.
    def assignDictionary(topologies, vertexGroup):
        for i, t in enumerate(topologies):
            if t in externalFaces:
                d1 = Dictionary.ByKeysValues(["id","group", "entity", "type", "area", "height"], [vertexGroup+str(i),vertexGroup, wallEntity, walltype, area, height])
                t = Topology.SetDictionary(t, d1)
            elif t in internalFaces:
                d1 = Dictionary.ByKeysValues(["id","group", "entity", "type", "area", "height"], [vertexGroup+str(i),vertexGroup, wallEntity, walltype, area, height])
                t = Topology.SetDictionary(t, d1)
            elif t in topFaces:
                d1 = Dictionary.ByKeysValues(["id","group", "entity", "type", "area", "height"], [vertexGroup+str(i),vertexGroup, slabEntity, slabtype2, area, height])
                t = Topology.SetDictionary(t, d1)
            elif t in bottomFaces:
                d1 = Dictionary.ByKeysValues(["id","group", "entity", "type", "area", "height"], [vertexGroup+str(i),vertexGroup, slabEntity, slabtype1, area, height])
                t = Topology.SetDictionary(t, d1)
            elif t in internalHorizFaces:
                d1 = Dictionary.ByKeysValues(["id","group", "entity", "type", "area", "height"], [vertexGroup+str(i),vertexGroup, slabEntity, slabtype1, area, height])
                t = Topology.SetDictionary(t, d1)
            elif t in externalInclinedFaces:
                d1 = Dictionary.ByKeysValues(["id","group", "entity", "type", "area", "height"], [vertexGroup+str(i),vertexGroup, roofEntity, slabtype2, area, height])
                t = Topology.SetDictionary(t, d1)
            else:
                d2 = Dictionary.ByKeysValues(["id","group"], [vertexGroup+str(i),vertexGroup])
                t = Topology.SetDictionary(t, d2)
    for vertexGroup in vertexGroups:
        topologies = d[vertexGroup]
        assignDictionary(topologies, vertexGroup)
            
    return (topologies, vertexGroups)

# # call
# building = create_face_dictionaries(building, selectors)
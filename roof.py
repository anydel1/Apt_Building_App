from topologicpy.Edge import Edge
from topologicpy.Wire import Wire
from topologicpy.Face import Face
from topologicpy.Cell import Cell
from topologicpy.CellComplex import CellComplex
from topologicpy.Cluster import Cluster
from topologicpy.Shell import Shell
from topologicpy.Topology import Topology
from topologicpy.Dictionary import Dictionary


# width = 8
# length = 10
# ridge_height = 3
# ridge_length = 6

def create_roof(topFace, bWidth, selectors, stHeight, ridge_height, ridge_length):
    # topFace = Face.Rectangle(width=width, length=length, direction=[0,0,1], placement="center")

    base_edges = Face.Edges(topFace)
    base_vertices = Face.Vertices(topFace)

    mid_edge = Edge.ByOffset2D(base_edges[1], bWidth/2,)
    ridge = Edge.TranslateByDirectionDistance(mid_edge, [0, 0, 1], ridge_height) # move to ridge height
    ridge = Edge.SetLength(ridge, ridge_length)

    # Group edges into equal lengths and ensure they are parallel
    edgeGroups = []
    lengths = [Edge.Length(edge) for edge in base_edges]  # Calculate lengths here
    for i in range(len(base_edges)):
        for j in range(i+1, len(base_edges)):
            if abs(lengths[i] - lengths[j]) < 0.0001 and Edge.IsParallel(base_edges[i], base_edges[j]):
                edgeGroups.append((base_edges[i], base_edges[j]))

    def create_edge(vertex1, vertex2):
        return Edge.ByStartVertexEndVertex(vertex1, vertex2)

    def create_face(edges):
        return Face.ByEdges(edges)

    vertices = [Edge.Vertices(edge) for edge in edgeGroups[0]]
    ridge_vertices = Edge.Vertices(ridge)

    slope_edges = [create_edge(vertex, ridge_vertices[i]) for i in range(2) for vertex in vertices[i]]

    # triangular faces
    endFaces = [create_face([edgeGroups[0][i], slope_edges[i*2], slope_edges[i*2+1]]) for i in range(2)]
    #sloped rectangle 1
    edges1 = [edgeGroups[1][0], slope_edges[1], slope_edges[2], ridge]
    slopeFace1 = create_face(edges1)

    # sloped rectangle 2
    edges2 = [edgeGroups[1][1], slope_edges[0], slope_edges[3], ridge]
    slopeFace2 = create_face(edges2)
        
    # assemble roof
    faces = [topFace, *endFaces, slopeFace1, slopeFace2]
    roof = Cell.ByFaces(faces)
    cen = Topology.Centroid(roof) # Find centroid

    # roof = Cluster.ByTopologies(base_rectangle, mid_edge, ridge)

    # Create dictionary     
    d4 = Dictionary.ByKeysValues(["id","group", "entity", "spaceID", "type", "area", "height", "volume"], ["Cells"+str(i), "Cells", "ifcSpace", "AT", "attic", 30, stHeight, 90])
    cen = Topology.SetDictionary(cen, d4)
    selectors.append(cen)

        # unitCells_attic = Cluster.ByTopologies(unitCells, attic)
        # building = CellComplex.ByCellsCluster(unitCells_attic)
        
    return(roof, selectors, stHeight)

# call
# roof, selectors, stHeight = create_roof(topFace, selectors, stHeight, ridge_height,)

# c = Cluster.ByTopologies(topFace, mid_edge, ridge)
# Topology.Show(c, vertexColor='red', vertexSize=3, renderer="browser")



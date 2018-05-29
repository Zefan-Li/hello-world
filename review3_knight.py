class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}
        self.distance = None
        self.predecessor = None
        self.color = None

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def getConnections(self):
        return self.connectedTo.keys()  # 这里的keys就直接是节点的引用了，value是这个路径的权重

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def setPred(self, vertex):
        self.predecessor = vertex

    def getPred(self):
        return self.predecessor

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def setDistance(self, d):
        self.distance = d

    def getDistance(self):
        return self.distance

    def __str__(self):
        return str(self.id) + ' connectedTo: '\
            + str([x.id for x in self.connectedTo])

    def __repr__(self):
        return self.__str__()


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices += 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            self.addVertex(f)
        if t not in self.vertList:
            self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def __iter__(self):
        return iter(self.vertList.values())


def knightGraph(bdSize):
    ktGraph = Graph()
    for row in range(bdSize):
        for col in range(bdSize):
            nodeId = posToNodeId(row, col, bdSize)
            newPositions = genLegalMoves(row, col, bdSize)
            for e in newPositions:
                nid = posToNodeId(e[0], e[1], bdSize)
                ktGraph.addEdge(nodeId, nid)
    return ktGraph  # 循环完成后自动构建了双向map


def genLegalMoves(x, y, bdSize):
    newMoves = []
    moveOffsets = [(-1, -2), (-1, 2), (-2, -1), (-2, 1),
                   (1, -2), (1, 2), (2, -1), (2, 1)]
    for i in moveOffsets:
        newX = x + i[0]
        newY = y + i[1]
        if legalCoord(newX, bdSize) and legalCoord(newY, bdSize):
            newMoves.append((newX, newY))
    return newMoves


def legalCoord(x, bdSize):
    if 0 <= x < bdSize:  # 这种简化的链式比较只适用于用 and 的情形
        return True
    else:
        return False


def posToNodeId(row, col, bdSize):
    return row * bdSize + col  # 因为从0开始刚刚好


def knightTour(n, path, u, limit):
    u.setColor('gray')
    path.append(u)
    if n < limit:
        nbrList = list(u.getConnections())
        i = 0
        done = False
        while i < len(nbrList) and not done:
            if nbrList[i].getColor() == 'white':
                done = knightTour(n + 1, path, nbrList[i], limit)
            i = i + 1
        if not done:
            path.pop()
            u.setColor('white')
    else:
        done = True
    return done


bdSize1 = 5
ktGraph1 = knightGraph(bdSize1)
print(ktGraph1.vertList)
path1 = []
for i in range(bdSize1 ** 2):
    out = knightTour(1, path1, ktGraph1.getVertex(i), bdSize1 ** 2)
    print(i)
    print(out)
    if out:
        print(path1)
    print()

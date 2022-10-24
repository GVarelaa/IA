class Node: 

    # construtor do nodo...
    def __init__(self, name):
        self.m_name = str(name)
        #colocar o objeto que o nodo vai referenciar, pode ser qualquer coisa

    def getName(self):
        return self.m_name

    def setName(self, name):
        self.m_name = name

    def __str__(self):
        return "node" + self.m_name
    
    def __eq__(self, other):
        # são iguais se nome igual, não usa o id
        return self.m_name == other.m_name

    def __hash__(self):
        return hash(self.m_name)
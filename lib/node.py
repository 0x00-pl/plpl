
def node_type():
    return tuple
def gen_node(data,name,textat=(0,0)):
    return (list(data),dict(name),('at',)+textat)
def node_data(node):
    return node[0]
def node_name(node):
    return node[1]
def node_textat(node):
    return node[2]

from node import *

def gen_innerdata(v):
    return (v,)
def is_innerdata(d):
    return type(d)==tuple
def innerdata(d):
    return d[0]

class sys_mempool:
    def gcnew(self,node):
        return node
    def getobj(self,dest):
        return dest
    def zipmem():
        pass
    def dump_node(self,uid):
       return uid
    def import_node(self,node):
       return node

class my_mempool:
    # type(uid)==int
    mem=[]
    def gcnew(self,node):
        self.mem.append(node)
        return len(self.mem)-1

    def getobj(self,dest):
        return self.mem[dest]

    def zipmem(self):
        pass
    
    def dump(self,uid):
        if is_innerdata(uid):
            return innerdata(uid)
        node= self.getobj(uid)
        data= node_data(node)
        name= node_name(node)
        if len(name)==0:
            return [self.dump(i) for i in data]
        else:
            autoname=[str(i) for i in range(len(data))]
            for n,i in name.items():
                autoname[i]=n
            return { autoname[i]:self.dump(data[i]) for i in range(len(data)) }

    def dump_node(self,uid):
        if is_innerdata(uid):
            return innerdata(uid)
        node= self.getobj(uid)
        return gen_node([self.dump_node(i) for i in node_data(node)], node_name(node), node_textat(node))

    def import_node(self,node):
        if type(node) == node_type():
            return self.gcnew(gen_node([self.import_node(i) for i in node_data(node)], node_name(node), node_textat(node)))
        else:
            return (node,)

    

if __name__=='__main__':
    import parser
    test_file_node= parser.read_all(open('../test/testfile.txt'))
    mp= my_mempool()
    root= mp.import_node(test_file_node)
    print('root: ',root)
    for i in range(len(mp.mem)):
        print(i, ' : ', mp.mem[i])

    print()
    node= mp.dump_node(root)
    print(str(node))    

    print()
    print(mp.dump(root))

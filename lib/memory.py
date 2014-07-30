import os
from node import *



class mempool:
    mem=[]
    name={}
    def gcnew(self,node):
        self.mem.append(node)
        return len(self.mem)-1

    def getobj(self,dest):
        return self.mem[dest]

    def name2uid(self,name):
        return self,name[str(name)]
    
    def zipmem(self):
        pass
    
    def dump(self,uid):
        if type(uid)==tuple:
            return uid[0]
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
        if type(uid)==tuple:
            return uid[0]
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
    mp=mempool()
    root=mp.import_node(test_file_node)
    print('root: ',root)
    for i in range(len(mp.mem)):
        print(i, ' : ', mp.mem[i])

    print()
    node= mp.dump_node(root)
    print(str(node))    

    print()
    print(mp.dump(root))

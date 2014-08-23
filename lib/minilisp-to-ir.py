from error import handle_err
from collections import Callable,Iterable

def isexp(v):
    return isinstance(v,Iterable) and type(v)!=str

# base of dbgmsg
class mempool_named:
    names={}
    
    def store(self,data,name=None):
        if name==None:
            return data
        elif isexp(data):
            for i in data:
                self.store(i)
            self.names[id(data)]=name
            return data
    def sortcat_store(self):
        def ret(*args,name=None):
            return store(self,args,name=name)
        return ret

    def export(self,uid):
        return uid

    def offset(self,uid,dot_name):
        name= self.names[id(uid)]
        return name[dot_name]

    def dot(self,uid,dot_name):
        return uid[self.offset(uid,dot_name)]
    

class ir:
    push_v,pop,\
    makelist_n,\
    call,ret,\
    skip_p,jn_p,entry,\
    *_=range(255)

    def make(*args):
        return args
    def to_str(line):
        f='unknow'
        for k,v in ir.__dict__.items():
            if v==line[0]:
                f=str(k)
                break
        return f+str(line[1:])
            
def pl_quote(mp,uid):
    ret=[]
    data= mp.export(uid)
    if not isexp(data):
        return [(ir.push_v,uid)]
    else:
        for arg_uid in data:
            ret.extend(pl_quote(mp,arg_uid))
        ret.append((ir.makelist_n,len(data)))
        return ret

def pl_compile_try_bulitin_func(mp,exp,ret):
    if len(exp)==0:
        ret.append((ir.push_v,None))
        return True
    f= mp.export(exp[0])
    if f=='cond':
        tmp_ir=[]
        need_to_link=[]
        for i in range(2,len(exp),2):
            tst= pl_compile(mp,exp[i-1])
            exp_i= pl_compile(mp,exp[i])

            tmp_ir.extend(tst)
            tmp_ir.append(( ir.jn_p, len(exp_i)+1 ))
            tmp_ir.extend(exp_i)
            need_to_link.append(len(tmp_ir))
            tmp_ir.append((ir.skip_p,None)) # jmp to end
            tmp_ir.append((ir.entry,))
        if len(exp)%2==0:
            tmp_ir.extend(pl_compile(mp,exp[-1]))
        tmp_ir.append((ir.entry,))
        tmp_ir_len= len(tmp_ir)
        for i in need_to_link:
            tmp_ir[i]= ( ir.skip_p, tmp_ir_len-i-2 )
        ret.extend(tmp_ir)
        return True
    elif f=='quote':
        for i in range(1,len(exp)):
            ret.extend(pl_quote(mp,exp[i]))
        ret.append((ir.makelist_n,len(exp)-1))
        return True
    else:
        return False

def pl_compile(mp,uid):
    ret=[]
    data= mp.export(uid)
    if not isexp(data):
        return [(ir.push_v,uid)]
    elif pl_compile_try_bulitin_func(mp,data,ret):
        pass
    else:
        for arg in data:
            ret= ret + pl_compile(mp,arg)
        ret= ret + [(ir.makelist_n,len(data)),(ir.call,)]
    return ret

if __name__=='__main__':
    import operator as op
    addn= ((("lambda", ('self','a'), 
                      ("lambda", ('self',"b",),(op.add, 'b', 'a')))
           ,(op.add,20,20))
          ,(op.add,1,1))

    fib=('lambda',('fib','a1','a2','n'),
         ('cond',(op.ge,2,'n'),'a2',
          True,('fib','a2',(op.add,'a1','a2'),(op.sub,'n',1))))
    exp= (fib,1,1,201)
    print(exp)
    print('----------')
    mp= mempool_named()
    for i in pl_compile(mp,('cond',('eq',1,2),('add',9,8),('quote','add',9,8))):
        print(ir.to_str(i))


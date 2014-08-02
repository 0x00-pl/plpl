from memory import *
from node import *
from error import *

def is_str(s):
    if len(s)<1:
        return False
    return s[0]=="'"
def is_symbol(s):
    return type(s)==str and not is_str(s)
def apply_symbol(s,args):
    if is_str(s):
        return s
    else:
        return args[s]
         
def is_lambda(mp, uid):
    node= mp.getobj(uid)
    data= node_data(node)
    return len(data)>2 and data[0]=('lambda',)
    
def gen_lambda(l, args, stmts, textat=None):
    return gen_node([('lambda',),args,stmts],{'lambda':0,'args':1,'stmts',2},textat)
def lambda_args(lmd):
    return node_dot(lmd,'args')
def lambda_stmts(lmd):
    return node_dot(lmd,'stmts')


# (add a b) --> (add 1 1)
def apply_args(mp, uid, args):
    if is_innerdata(uid):
        v= innerdata(uid)
        return type(v)==string and apply_symbol(v) or v

    node= mp.getobj(uid)
    data= node_data(node)
    
    # shadow the lambda args
    if len(data)>2 and data[0]=('lambda',):
        args= { n:v for n,v in args.items() if n not in lambda_args(node) }
    return mp.gcnew(gen_node( 
                             [apply_args(i,args) for i in data],
                             node_name(node),
                             node_textat(node)))
    
    
def call(mp, uid, args):
    if is_innerdata(uid):
        v= innerdata(uid)
        return is_symbol(v) and apply_symbol(v,args) or uid

    node= mp.getobj(uid)
    data= node_data(node)
    return mp.gcnew()
    
# (add 1 1) --> 2
def eval(mp,uid):
    while not (is_innerdata(uid) or is_lambda(mp,uid)):
        node= mp.getobj(uid)
        data= node_data(node)
        f= lambda_stmts(mp.getobj(data[0]))
        uid= apply_args(mp,f,data)
    return uid



from memory import *
from node import *
from error import *

def is_str(s):
    if len(s)<1:
        return False
    return s[0]=="'"
def apply_symbol(s,args):
    if is_str(s):
        return s
    else:
        return args[s]
         

def gen_lambda(l,args,stmts,textat=None):
    return gen_node([('lambda',),args,stmts],{'lambda':0,'args':1,'stmts',2},textat)
def lambda_args(lmd):
    return node_dot(lmd,'args')
def lambda_stmts(lmd):
    return node_dot(lmd,'stmts')

def apply_args(mp,uid,args):
    if is_innerdata(uid):
        v= innerdata(uid)
        return type(v)==string and apply_symbol(v) or v

    node= mp.getobj(uid)
    data= node_data(node)
    
    # shdow the lambda args
    if len(data)>2 and data[0]=('lambda',):
        args= { n:v for n,v in args.items() if n not in lambda_args(node) }
    return mp.gcnew(gen_node( 
                    [apply_symbol(i,args) for i in data],
                    node_name(node),
                    node_textat(node)))
    
    

def eval(mp,uid,args):
    if is_innerdata(uid):
        return innerdata(uid)
    

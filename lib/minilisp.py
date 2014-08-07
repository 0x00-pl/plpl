from error import handle_err
from collections import Callable,Iterable

def is_symbol(s):
    return type(s)==str and s[:1]!="'"
def is_lambda(l):
    if not isinstance(l,Iterable):
        return False
    try:
        s,args,exp=l
        return s=="lambda"
    except ValueError:
        return False

def apply(exp, env):
    if is_symbol(exp):
        return env.get(exp,exp)
    if type(exp)==str or not isinstance(exp,Iterable):
        return exp
    if is_lambda(exp):
        env= { k:v for k,v in env.items() if k not in exp[1] }
    return len(env)>0 and tuple( apply(i,env) for i in exp ) or exp

def eval(l):
    if isinstance(l,Iterable):
        if l[0]=='cond':
            for i in range(2,len(l),2):
                if eval(l[i-1]):
                    return eval(l[i])
            return len(l)%2==0 and eval(l[-1])			
           
    if type(l)==str or\
       isinstance(l,Callable) or\
       is_lambda(l) or\
       not isinstance(l,Iterable):
        return l
    else:
        return eval_inner(*l)

def eval_inner(f,*args):    
    f= eval(f)
    args= tuple( eval(i) for i in args )
    
    if isinstance(f,Callable):
        return f(*args)
    if is_lambda(f):
        _,names,exp= f
        tail= apply(exp,dict(zip(names, (f,)+args)))
        return eval(tail)
    handle_err(str(f)+'is not a function.')

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
    print(eval(exp))


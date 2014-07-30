import os
from error import *
from node import *

# global value
line=1
col=0
char=0

ln0='\r\n'
space0=' \t'+ln0
def read_space(it):    
    global line
    global col
    global char
    while True:
        c=next(it,None)
        if c==None:
            return ''
        if c not in space0:
            it.send(True) # undo next(it)
            return ' '
        if c in ln0:
            line+=1
            col=0

number0='+-.0123456789'
number1=number0+'eE'
def read_number(it):    
    global line
    global col
    global char
    buf=''
    while True:
        c=next(it)
        if c in number1:
            buf=buf+c
        else:
            it.send(True) # undo next(it)
            return float(buf)

string0='"'
def read_string(it):    
    global line
    global col
    global char
    ret=''
    c=next(it,'"')
    if c!='"':
        handle_err(str({'line':line,'col':col})+':: not a string.')
    while True:
        c=next(it)
        if c=='\\':
            c=next(it)
            if c=='\n':
                line+=1
                col=0
            elif c=='u':                    
                u1=next(it)
                u2=next(it)
                u3=next(it)
                u4=next(it)
                us='\\u'+u1+u2+u3+u4
                ret=ret+ us.encode('iso-8859-1').decode("unicode-escape")
            else:
                ret=ret+{
                    '"':'"',
                    '\\':'\\',
                    '/':'/',
                    'b':'\b',
                    'f':'\f',
                    'n':'\n',
                    'r':'\r',
                    't':'\t'
                    }[c]
        elif c=='"':
            return ret
        else:
            ret=ret+c


array0='['
def read_array(it):
    global line
    global col
    global char
    data=[]
    textat=(line,col)
    
    c=next(it)
    if c!='[':
        handle_err(str({'line':line,'col':col})+':: not a array.')
        
    while True:
        read_space(it)
        c=next(it,']')
        if c==']':
            return gen_node(data,{},textat)
        it.send(True) # undo next(it)

        read_space(it)
        cur_data= read_value(it)
        data.append(cur_data)

        read_space(it)
        c=next(it,']')
        if c==']':
            it.send(True) # undo next(it)
            continue
        if c!=',':
            handle_err(str({'line':line,'col':col})+':: not a array.\
 unknow charcher: '+c+' missing "," ?')
        
object0='{'
def read_object(it):    
    global line
    global col
    global char
    data=[]
    name={}
    textat=(line,col)

    c=next(it)
    if c!='{':
        handle_err(str({'line':line,'col':col})+':: not a object.')
    while True:
        read_space(it)
        c=next(it,'}')
        if c=='}':
            return gen_node(data,name,textat)
        
        cur_name='$unparsed_string$'
        if c in string0:
            it.send(True) # undo next(it)
            cur_name= read_string(it)
        else:
            handle_err(str({'line':line,'col':col})+':: not a string.')
        
        read_space(it)
        c=next(it)
        if c!=':':
            handle_err(str({'line':line,'col':col})+':: not a object.')

        read_space(it)
        cur_data= read_value(it)
        name[cur_name]= len(data)
        data.append(cur_data)

        read_space(it)
        c=next(it,'}')
        if c=='}':
            it.send(True) # undo next(it)
            continue
        if c!=',':
            handle_err(str({'line':line,'col':col})+':: not a object.')


def read_value(it):    
    global line
    global col
    global char
    read_space(it)
    c=next(it)
    it.send(True) # undo next(it)
    if c in string0:
        return read_string(it)
    elif c in number0:
        return read_number(it)
    elif c in object0:
        return read_object(it)
    elif c in array0:
        return read_array(it)
    #elif c in (T,F,N): #bool
    handle_err(str({'line':line,'col':col})+':: unknowe Type.'+c)

def read_all(code_iter):
    def by_char(fs):
        global char
        global col
        for ln in fs:
            for c in ln:
                while (yield c): # .send(True) to read last char
                    yield None # yield to .send
                char+=1
                col+=1
    code_iter=by_char(code_iter)
    
    global line
    global col
    global char
    line=1
    col=0
    char=0
    
    return read_value(code_iter)



if __name__=='__main__':
    print(str(read_all(open('F:\\git\\plpl\\test\\testfile.txt'))))
    print(str(read_all('{"testme":"ok"}')))
    print(str(read_all(['{"testme2"',':','"ok"}'])))
    

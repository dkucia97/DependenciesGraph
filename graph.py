import networkx 
import matplotlib.pyplot 
import os
from os import listdir
import sample
from tkinter import *
import tkinter.filedialog as filedialog
import re

def loadFolder():
    root=Tk()
    #opens file manager
    path=filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
    root.destroy()
    return path

def createGraph(path="./"):
    g=networkx.DiGraph() # create direct graph 
    files_to_parse=get_python_files(path) #only python files
    
    for file in files_to_parse:
        g.add_node(extract_filename(file),waga = extract_filesize(file,g,path))
        find_edges_in_file(file,g,path)

    matplotlib.pyplot.figure()
    pos = networkx.spring_layout(g)
    networkx.draw(g,pos, with_labels=True, font_weight='bold')
    
    pos_attr = {}
    for node, coords in pos.items():
        pos_attr[node] = (coords[0], coords[1] +00.07)
    
    node_attr = networkx.get_node_attributes(g, 'waga')
    custom_node_attrs = {}
    for node, attr in node_attr.items():
        custom_node_attrs[node] = str(attr)

    networkx.draw_networkx_labels(g,pos_attr, labels=custom_node_attrs)

    edge_labels = dict([((u,v),d['weight']) for u,v,d in g.edges(data=True)])
    networkx.draw_networkx_edge_labels(g,pos,edge_labels = edge_labels)
    
    matplotlib.pyplot.show()

def find_edges_in_file(file,g,path):
    with  open(path+"/"+file, 'r') as fr:
        for number, line in enumerate(fr):
            if("from" in line):
                tab=line.split()
                if(tab[0]=="from"):
                    w = sample.count_import(file,tab[1])
                    g.add_edge(extract_filename(file),tab[1], weight = w)
            elif("import" in line):
                tab=line.split()
                if(tab[0]=="import"):
                    w = sample.count_import(file,tab[1])
                    print(w)
                    g.add_edge(extract_filename(file),tab[1],weight = w)

            
def extract_filename(file):
    return file.split(".")[0]  #cut extension .py


def extract_filesize(file,g,folderPath):
    return os.path.getsize(folderPath+"/"+file)


def get_python_files(path):
    return list(filter(lambda f: f.endswith(".py") ,listdir(path)))

def create_function_graph(path="./"):
    g=networkx.DiGraph() # create direct graph 
    files_to_parse=get_python_files(path) #only python files
    allFunctions=[]
    tmpFunctions=[]
    #creating nodes
    for file in files_to_parse:
        allFunctions+=get_functions_names_from_file(path+"/"+file)
        tmpFunctions=get_functions_names_from_file(path+"/"+file)
        for fun in tmpFunctions:
            g.add_node(fun,waga = count_method_size(path+"/"+file,fun))
    #creating edges
    for file in files_to_parse:
        for fun in allFunctions :
            for otherFun in allFunctions:
                methodCount=count_method(path+"/"+file,fun,otherFun)
                if(methodCount>0):
                    g.add_edge(fun,otherFun,weight = methodCount)

    ##  labels copied from other graph
    matplotlib.pyplot.figure()
    pos = networkx.spring_layout(g)
    networkx.draw(g,pos, with_labels=True, font_weight='bold')
    
    pos_attr = {}
    for node, coords in pos.items():
        pos_attr[node] = (coords[0], coords[1] +00.07)
    
    node_attr = networkx.get_node_attributes(g, 'waga')
    custom_node_attrs = {}
    for node, attr in node_attr.items():
        custom_node_attrs[node] = str(attr)

    edge_labels = dict([((u,v),d['weight']) for u,v,d in g.edges(data=True)])
    networkx.draw_networkx_edge_labels(g,pos,edge_labels = edge_labels)

    networkx.draw_networkx_labels(g,pos_attr, labels=custom_node_attrs)
    ##
    matplotlib.pyplot.show()


def get_functions_names_from_file(path):
    res=[]
    with open(path, 'r') as fr:
         for number, line in enumerate(fr):
             if re.match(r"^\s*?def",line) :
                 res.append(line.split(" ")[1].split("(")[0])
    return res

def count_method(path, method, otherMethod):
    count = 0
    t = 0
    str = 'def ' + method
    f = open(path,"r")
    for x in f:
        if t == 1:
            if 'def ' in x:
                t = 0
                f.close()
                return count
            if otherMethod in x:
                count=count+1
        elif str in x:
            t = 1    
    f.close()
    return count

def count_method_size(path, method): #returns function line count
    count = 0
    t = 0
    str = 'def ' + method
    f = open(path,"r")
    for x in f:
        if t == 1:
           if 'def ' in x:
                t = 0
                return count
           count=count+1   
        elif str in x:
            t = 1    
    f.close()
    return count

def count_method1(path, method):
    count = 0
    f = open(path,"r")
    for x in f:
        if method in x:
            count = count + 1
    f.close()
    return count

def createFunModuleGraph(path="./"):
    g=networkx.DiGraph() # create direct graph 
    files_to_parse=get_python_files(path) #only python files
    tmp_f_t_p = files_to_parse
    print(tmp_f_t_p)
    for file in files_to_parse:
        count = 0
        this_file = file
        list_of_file_fun = get_functions_names_from_file(file)
        #
        for func in list_of_file_fun:
            for fl in files_to_parse:
                if fl == this_file:
                    g.add_node(func)
                else:
                    count = count + count_method1(path+"/"+fl, func)
        g.add_node(extract_filename(file),weight = count)
        count = 0

    for file in tmp_f_t_p:
        count = 0
        this_file = file
        list_of_file_fun = get_functions_names_from_file(file)
        print(list_of_file_fun)
        for func in list_of_file_fun:
            for fl in tmp_f_t_p:
                if fl == this_file:
                    tmp_count = count_method1(path+"/"+fl, func)
                    g.add_edge(func, extract_filename(file),weight = tmp_count)
                else:
                    count = count_method1(path+"/"+fl, func) + count_method1(path+"/"+file, func)
        
        g.add_edge(extract_filename(file),extract_filename(fl),weight = count)
        
        

    matplotlib.pyplot.figure()
    pos = networkx.spring_layout(g)
    networkx.draw(g,pos, with_labels=True, font_weight='bold')
    
    pos_attr = {}
    for node, coords in pos.items():
        pos_attr[node] = (coords[0], coords[1] +00.07)
    
    node_attr = networkx.get_node_attributes(g, 'weight')
    custom_node_attrs = {}
    for node, attr in node_attr.items():
        custom_node_attrs[node] = str(attr)

    edge_labels = dict([((u,v),d['weight']) for u,v,d in g.edges(data=True)])
    networkx.draw_networkx_edge_labels(g,pos,edge_labels = edge_labels)

    networkx.draw_networkx_labels(g,pos_attr, labels=custom_node_attrs)
    ##
    matplotlib.pyplot.show()






createFunModuleGraph(loadFolder())

#createGraph(loadFolder())
create_function_graph(loadFolder())

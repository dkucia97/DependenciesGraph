import networkx 
import matplotlib.pyplot 
import os
from os import listdir
import sample
from tkinter import *

def loadFolder():
    root=Tk()
    #opens file manager
    path=filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
    root.destroy()
    return path

def createGraph(path=loadFolder()):
    g=networkx.DiGraph() # create direct graph 
    files_to_parse=list(filter(lambda f: f.endswith(".py") ,listdir(path))) #only python files
    
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


createGraph()

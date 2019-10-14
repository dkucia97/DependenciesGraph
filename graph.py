import networkx as nx
import matplotlib.pyplot as plt
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
    g=nx.DiGraph() # create direct graph 
    files_to_parse=list(filter(lambda f: f.endswith(".py") ,listdir(path))) #only python files
    for file in files_to_parse:
        g.add_node(extract_filename(file))
        find_edges_in_file(file,g,path)
    return g
   


def drawGraph(graph):
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()


def find_edges_in_file(file,g,path):
    with  open(path+"/"+file, 'r') as fr:
        for number, line in enumerate(fr):
            if("from" in line):
                tab=line.split()
                if(tab[0]=="from"):
                    g.add_edge(extract_filename(file),tab[3])
            elif("import" in line):
                tab=line.split()
                if(tab[0]=="import"):
                    g.add_edge(extract_filename(file),tab[1])

            
def extract_filename(file):
    return file.split(".")[0]  #cut extension .py

g=createGraph()
drawGraph(g)
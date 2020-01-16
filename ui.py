from tkinter import *
import matplotlib.pyplot
import graph
import networkx
import sample


def button1():
    graph.createFunModuleGraph(lf)
    matplotlib.pyplot.show()

def button2():
    graph.create_function_graph(lf)
    matplotlib.pyplot.show()

def button3():
    graph.createGraph(lf)
    matplotlib.pyplot.show()

def button4():
    graph.createFunModuleGraph(lf)
    graph.create_function_graph(lf)
    graph.createGraph(lf)
    matplotlib.pyplot.show()

lf=graph.loadFolder()


listOfFunNames,listOfFunCC=sample.count_cyclomatic_complexity(lf)
#kontrolne printfy
for item in listOfFunNames:
    print(item)
for item in listOfFunCC:
    print(item)

root=Tk()
    
topFrame=Frame(root)
topFrame.pack()
bottomFrame=Frame(root)
bottomFrame.pack(side=BOTTOM)


fileGraphButton=Button(topFrame,text="File Graph", fg = "red", command=button1)
methodGraphButton=Button(topFrame,text="Method Graph", fg="blue", command=button2)
packageGraphButton=Button(topFrame,text="Package Graph",fg="green", command=button3)
oneToRuleThemAllButton=Button(bottomFrame,text="One To Rule Them All", fg ="purple", command=button4)

fileGraphButton.pack(side=LEFT)
methodGraphButton.pack(side=LEFT)
packageGraphButton.pack(side=LEFT)
oneToRuleThemAllButton.pack(side=BOTTOM)

root.mainloop()
#print("xd")
#matplotlib.pyplot.show()
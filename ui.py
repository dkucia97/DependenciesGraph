from tkinter import *
import matplotlib.pyplot
import graph
import networkx
import sample
import git
repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha

def button1():
    graph.createFunModuleGraph(lf,listOfFunNames,listOfFunCC)
    matplotlib.pyplot.show()

def button2():
    graph.create_function_graph(lf,listOfFunNames,listOfFunCC)
    matplotlib.pyplot.show()

def button3():
    graph.createGraph(lf)
    matplotlib.pyplot.show()

def button4():
    graph.createFunModuleGraph(lf,listOfFunNames,listOfFunCC)
    graph.create_function_graph(lf,listOfFunNames,listOfFunCC)
    graph.createGraph(lf)
    matplotlib.pyplot.show()



lf=graph.loadFolder()


listOfFunNames,listOfFunCC=sample.count_cyclomatic_complexity(lf)
#kontrolne printfy
#for item in listOfFunNames:
#    print(item)
#for item in listOfFunCC:
#    print(item)

root=Tk()
    
topFrame=Frame(root)
topFrame.pack()
bottomFrame=Frame(root)
bottomFrame.pack(side=BOTTOM)

T = Text(bottomFrame, height=2, width=30)
T.pack()
T.insert(INSERT, "Git ver. hash: \n")
T.insert(END, sha)
fileGraphButton=Button(topFrame,text="File Graph", fg = "red", command=button1)
methodGraphButton=Button(topFrame,text="Method Graph", fg="green", command=button2)
packageGraphButton=Button(topFrame,text="Package Graph",fg="blue", command=button3)
oneToRuleThemAllButton=Button(bottomFrame,text="One To Rule Them All", fg ="purple", command=button4)

fileGraphButton.pack(side=LEFT)
methodGraphButton.pack(side=LEFT)
packageGraphButton.pack(side=LEFT)
oneToRuleThemAllButton.pack(side=BOTTOM)
T.pack(side=BOTTOM)

root.mainloop()
#print("xd")
#matplotlib.pyplot.show()
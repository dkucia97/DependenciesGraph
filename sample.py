import graph
import os


def count_import(file, name):
    tmp = 0
    f = open(file,"r")
    for x in f:
        if name in x:
            tmp = tmp + 1
    f.close()
    return tmp


def count_cyclomatic_complexity(path):
    listOfFiles = graph.get_python_files(path)
    os.chdir(path)
    bigList=[]
    for item in listOfFiles:
        #os.system("radon cc "+item+" -s")
        p = os.popen("radon cc "+item+" -s",'r',1)
        bigList.append(p.read())
        p.close()

    listOfLines=[]
    for item in bigList:
        a=item.splitlines()
        for line in a:    
            listOfLines.append(line)

    listOfFunNames=[]
    listOfFunCC=[]
    for item in listOfLines:
        if(item.find(" F ")>-1):
            listOfFunNames.append(item.split()[2])
            listOfFunCC.append(int(item.split()[5].split("(")[1].split(")")[0]))

    return listOfFunNames,listOfFunCC

def count_library(file):
    toRet = []
    f = open(file,"r")
    for x in f:
        if "import " in x:
            toRet.append(x.split(' ')[1].split(' ')[0])
    return toRet

def import_list(file):
    importList = count_library(file)
    valueList = []
    fileList = [file,importList]
    for t in importList:
        valueList.append(count_import(file,t))
    fileList.append(valueList)
    return fileList

file = "graph.py"
name = "nx."
val = count_import(file,name)
print(val)

l = import_list(file)
print(l)


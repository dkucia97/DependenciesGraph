def count_import(file, name):
    tmp = 0
    f = open(file,"r")
    for x in f:
        if name in x:
            tmp = tmp + 1
    f.close()
    return tmp

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


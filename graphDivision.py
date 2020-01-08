
import networkx
import matplotlib.pyplot
import graph
matplotlib.pyplot.figure()

def get_max(fun_dic):
    val_max = 0
    guard = 1
    for x in range(len(fun_dic) + 1):
        if x is not 0:
            tmp = fun_dic.get(x)
            print("tmp :" + str(tmp))
            b = str(tmp).split(': ')[1].split("}")[0]
            c = int(b)
            print(type(c))
            if c > val_max:
                val_max = c
                guard = x
    toret = fun_dic.get(guard)
    fun1 = str(toret).split("'")[1].split("'")[0]
    fun2 = str(toret).split(" '")[1].split("',")[0]
    fun_dic.pop(guard)
    return val_max, fun1, fun2

def division(path="./"):
    g1 = networkx.DiGraph()  # create direct graph
    g2 = networkx.DiGraph()  # create direct graph
    g3 = networkx.DiGraph()  # create direct graph
    files_to_parse = graph.get_python_files(path)  # only python files
    allFunctions = []
    fun_dic = {}
    tmpFunctions = []
    # creating nodes
    for file in files_to_parse:
        allFunctions += graph.get_functions_names_from_file(path + "/" + file)
        tmpFunctions = graph.get_functions_names_from_file(path + "/" + file)
    #    for fun in tmpFunctions:
     #       g.add_node(fun, waga=graph.count_method_size(path + "/" + file, fun))
    # creating edges
    i = 1
    for file in files_to_parse:
        for fun in allFunctions:
            if fun != "":

                for otherFun in allFunctions:
                    methodCount = graph.count_method(path + "/" + file, fun, otherFun)
                    if (methodCount > 0):
                        #g.add_edge(fun, otherFun, weight=methodCount)
                        if otherFun != "" and otherFun != fun:
                            dic = {i: (fun, otherFun, {"nr": methodCount})}
                            fun_dic.update(dic)
                            i = i + 1
    print(fun_dic.items())
    i = 1
    while fun_dic:
        x, f1, f2 = get_max(fun_dic)
        print(x,f1,f2)
        if i == 1:
            g1.add_node(f1)
            g1.add_node(f2)
            g1.add_edge(f1,f2,weight=x)
        if i == 2:
            g2.add_node(f1)
            g2.add_node(f2)
            g2.add_edge(f1,f2,weight=x)
        if i == 3:
            g3.add_node(f1)
            g3.add_node(f2)
            g3.add_edge(f1, f2, weight=x)
        i = i + 1
        if i == 4:
            i = 1
    ##  labels copied from other graph
    # matplotlib.pyplot.figure()
    pos1 = networkx.spring_layout(g1, center=[2, 1])
    pos2 = networkx.spring_layout(g2, center=[3, 2])
    pos3 = networkx.spring_layout(g3, center=[4, 3])
    color_map1 = []
    color_map2 = []
    color_map3 = []
    for node in g1:
        color_map1.append("green")
    networkx.draw(g1, pos1, node_color=color_map1, with_labels=True, font_weight='bold')
    for node in 2:
        color_map2.append("red")
    networkx.draw(g2, pos2, node_color=color_map2, with_labels=True, font_weight='bold')
    for node in g2:
        color_map3.append("yellow")
    networkx.draw(g3, pos3, node_color=color_map3, with_labels=True, font_weight='bold')

    pos_attr1 = {}
    pos_attr2 = {}
    pos_attr3 = {}
    for node, coords in pos1.items():
        pos_attr1[node] = (coords[0], coords[1] + 00.07)
    for node, coords in pos2.items():
        pos_attr2[node] = (coords[0], coords[1] + 00.07)
    for node, coords in pos3.items():
        pos_attr3[node] = (coords[0], coords[1] + 00.07)

    node_attr1 = networkx.get_node_attributes(g1, 'waga')
    node_attr2 = networkx.get_node_attributes(g2, 'waga')
    node_attr3 = networkx.get_node_attributes(g3, 'waga')
    custom_node_attrs1 = {}
    custom_node_attrs2 = {}
    custom_node_attrs3 = {}
    for node, attr in node_attr1.items():
        custom_node_attrs1[node] = str(attr)
    for node, attr in node_attr2.items():
        custom_node_attrs2[node] = str(attr)
    for node, attr in node_attr3.items():
        custom_node_attrs3[node] = str(attr)

    edge_labels1 = dict([((u, v), d['weight']) for u, v, d in g1.edges(data=True)])
    edge_labels2 = dict([((u, v), d['weight']) for u, v, d in g2.edges(data=True)])
    edge_labels3 = dict([((u, v), d['weight']) for u, v, d in g3.edges(data=True)])

    networkx.draw_networkx_edge_labels(g1, pos1, edge_labels=edge_labels1)
    networkx.draw_networkx_edge_labels(g2, pos2, edge_labels=edge_labels2)
    networkx.draw_networkx_edge_labels(g3, pos3, edge_labels=edge_labels3)

    networkx.draw_networkx_labels(g1, pos_attr1, labels=custom_node_attrs1)
    networkx.draw_networkx_labels(g2, pos_attr2, labels=custom_node_attrs2)
    networkx.draw_networkx_labels(g3, pos_attr3, labels=custom_node_attrs3)


lf = graph.loadFolder()
division(lf)
matplotlib.pyplot.show()
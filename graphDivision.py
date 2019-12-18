
import networkx
import matplotlib.pyplot
import graph

def division(path="./"):
    g=networkx.DiGraph() # create direct graph
    files_to_parse=graph.get_python_files(path) #only python files
    tmp_f_t_p = files_to_parse
    print(tmp_f_t_p)
    for file in files_to_parse:
        count = 0
        this_file = file
        list_of_file_fun = graph.get_functions_names_from_file(file)
        #
        for func in list_of_file_fun:
            for fl in files_to_parse:
                if fl == this_file:
                    g.add_node(func, weight=graph.count_method_size(path+"/"+file,func))
                else:
                    count = count + graph.count_method1(path+"/"+fl, func)
        g.add_node(graph.extract_filename(file),weight = count)
        count = 0

    for file in tmp_f_t_p:
        count = 0
        this_file = file
        list_of_file_fun = graph.get_functions_names_from_file(file)
        print(list_of_file_fun)
        for func in list_of_file_fun:
            for fl in tmp_f_t_p:
                if fl == this_file:
                    tmp_count = graph.count_method1(path+"/"+fl, func)
                    g.add_edge(func, graph.extract_filename(file),weight = tmp_count)
                else:
                    count = graph.count_method1(path+"/"+fl, func) + graph.count_method1(path+"/"+file, func)

        g.add_edge(graph.extract_filename(file),graph.extract_filename(fl),weight = count)

    matplotlib.pyplot.figure()
    pos = networkx.spring_layout(g, center = [0,2])
    color_map = []
    for node in g:
        color_map.append("red")
    networkx.draw(g,pos,node_color = color_map, with_labels=True, font_weight='bold')

    pos_attr = {}
    for node, coords in pos.items():
        pos_attr[node] = (coords[0], coords[1] + 00.05)

    node_attr = networkx.get_node_attributes(g, 'weight')
    custom_node_attrs = {}
    for node, attr in node_attr.items():
        custom_node_attrs[node] = str(attr)

    edge_labels = dict([((u,v),d['weight']) for u,v,d in g.edges(data=True)])
    networkx

    networkx.draw_networkx_edge_labels(g,pos,edge_labels = edge_labels)

    networkx.draw_networkx_labels(g,pos_attr, labels=custom_node_attrs)
    matplotlib.pyplot.show()

lf = graph.loadFolder()
division(lf)
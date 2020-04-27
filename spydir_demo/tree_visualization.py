# to run the visualizer in scrape_driver.py
# import tree_visualization as tv
# call tv.gen_tree(returnedList, <filename>)

import graphviz as gv

# creates a set of links from the list of dictionaries
# used for obtaining all unique links
def create_set(dict_list):
    dict_set = set()

    for d in dict_list:
        dict_set.add(d["url_from"])
        dict_set.add(d["url_to"])

    return dict_set

# converts the list of dictonaries returned by ScraPy into an organized list of dictionaries where each key maps to a list of links
# ex. "piazza.com": ["piazza.com/cs", "piazza.com/login"]
def create_organized_dict(dict_list):
    dict_set = create_set(dict_list)

    organized_dict = {}
    for d in dict_set:
        organized_dict[d] = list()

    for d in dict_list:
        organized_dict[d["url_from"]].append(d["url_to"])

    return organized_dict

# generates the visualized tree and saves it to a .png file
def gen_tree(dict_list, filename):
    organized_dict = create_organized_dict(dict_list)

    tree = gv.Digraph(filename, format="png", graph_attr={"ranksep":"5", "rankdir":"LR", "ratio":"auto", "splines":"polyline"},
                                    node_attr={'color': 'lightblue2', 'style': 'filled', "height":"1", "fontsize":"20"})
    count = 0
    for parent in organized_dict:
        with tree.subgraph(name=""+str(count), ) as s:
            s.graph_attr["rankdir"] = "LR"
            s.graph_attr["style"] = "invis"

            if count == 0:
                s.attr(rank="min")
            elif count == len(organized_dict)-1:
                s.attr(rank="same")

            count += 1
            for child in organized_dict[parent]:
                s.edge(parent[6:], child[6:])

    tree.graph_attr["levels"] = str(count)

    tree.render()
    tree.view()

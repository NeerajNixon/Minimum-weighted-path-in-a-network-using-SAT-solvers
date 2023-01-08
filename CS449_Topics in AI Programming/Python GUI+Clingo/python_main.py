from tkinter import *
import numpy as np

# Global variables --------------------------------------------------------------

from_list = []
to_list = []
edgeweight = []
node_list = []
pathends = []

#----------------------------------------------------------------------------------

root = Tk()
root.title("GUI interface for Topology")

label1 = Label(root, text=" Enter the number of nodes in the topography ")
label1.grid(row=1 , column=0)
label2 = Label(root, text = "Enter the connections in the topography ")
label2.grid(row = 2, column = 0)
label3 = Label(root, text= "Enter the endpoints of the required path")
label3.grid(row = 3, column = 0)

# Inputs ---------------------------------------------------------------------------

nums = Entry(root, width = 50, borderwidth = 5)
nums.grid(row = 1, column = 1)
nodes = Entry(root, width = 50,borderwidth = 5)
nodes.grid(row = 2,column = 1)
endpoints = Entry(root, width = 50, borderwidth = 5)
endpoints.grid(row = 3,column = 1)


# Functions -------------------------------------------------------------------------

def on_click():

    global from_list
    global to_list
    global edgeweight
    global pathends
    global node_list

    number_of_nodes = int(nums.get())
    req_nodes = nodes.get()
    ends = endpoints.get()

# Creating the node_list ---------------------------------------------------------------

    int_lists = []

    for i in range(1, number_of_nodes+1):
        int_lists.append(i)

    node_list = np.char.mod('%d', int_lists)

# Creating the from and to lists ---------------------------------------------------------
    
    new = [int(x) for x in req_nodes.split()]
    pathends = [int(y) for y in ends.split()]

    for i in new[::3]:
        from_list.append(i)
    from_list = np.char.mod('%d', from_list)

    for j in new[1::3]:
        to_list.append(j)
    to_list = np.char.mod('%d', to_list)

    for j in new[2::3]:
        edgeweight.append(j)
    edgeweight = np.char.mod('%d', edgeweight)

    print(from_list)
    print(to_list)
    print(edgeweight)

# Plotting the nodes and Edges ----------------------------------------------------------

    import networkx as nx
    import plotly.graph_objs as go

    G = nx.Graph()
    for i in range(number_of_nodes):
        G.add_node(node_list[i])

    for p in range(0,len(to_list)):
        G.add_edges_from([(from_list[p], to_list[p])])

    pos = nx.spring_layout(G, k=0.5, iterations=100)
    for n, p in pos.items():
        G.nodes[n]['pos'] = p

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    #---------------------------------------------------------------------------------

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            colorscale='pinkyl',
            reversescale=False,
            color=[],
            size=37,
            line=dict(width=0)))
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'] += tuple([len(adjacencies[1])])
        node_info = adjacencies[0]
        node_trace['text'] += tuple([node_info])

    # Outputting the required topology -----------------------------------------------------------------

    title = "Network Topology"
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                    title=title,
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=21, l=5, r=5, t=40),
                    annotations=[dict(
                        text=" ",
                        showarrow=False,
                        xref="paper", yref="paper")],
                    xaxis=dict(showgrid=False, zeroline=False,
                            showticklabels=False, mirror=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, mirror=False)))
    fig.show()

#Button for submitting response

Button(root, text = "Submit ", command = on_click).grid(row=4, column=1)

root.mainloop()

#------------------------------------------------------------------------------------










#                                       BREAK









#---------------------------------------------------------------------------------------



# Integrating Clingo

import clingo

from_list2 = []
to_list2 = []
newnode = []


def answer(ans):
    # Creating the from and to lists

    global from_list2
    global to_list2
    global newnode


    from_list2 = []
    to_list2 = []
    newnode = []
  

    atoms=ans.symbols(atoms=True)
    for atom in atoms:
        if str(atom.name)=="nod":
            s=str(atom.arguments[0])
            newnode = np.append(newnode,s)
        elif str(atom.name)=="con":
            s=str(atom.arguments[0])
            from_list2 = np.append(from_list2,s)
            b=str(atom.arguments[1])
            to_list2 = np.append(to_list2,b)
       
        else:
            continue

    if len(from_list2)>1:
        for i in range(len(from_list2)):
            if ((int(from_list2[i])==pathends[0] and int(to_list2[i])==pathends[1]) or (int(from_list2[i])==pathends[1] and int(to_list2[i])==pathends[0])):
                from_list2=np.delete(from_list2,i)
                to_list2=np.delete(to_list2,i)
                break


    print(newnode)
    print(from_list2)
    print(to_list2)
    print(pathends)



# Writing file into Clingo -----------------------------------------------------------

ctl=clingo.Control("0")
with open("data1.lp",'w') as f:
    for i in node_list:
        f.write("node("+i+").")
    for j in range(0,len(from_list)):
        f.write("connect("+str(from_list[j])+","+str(to_list[j])+","+str(edgeweight[j])+").")
    f.write("path("+str(pathends[0])+","+str(pathends[1])+").")
ctl.load("data1.lp")
ctl.load("clin.lp")
ctl.configuration.solve.models="0"
ctl.ground([("base",[])])

with ctl.solve(on_model=lambda m: answer(m),async_=True) as handle:
    while not handle.wait(0):pass
    handle.get()
 
# Plotting Shortest path --------------------------------------------------------------

import networkx as nx
import plotly.graph_objs as go

G2 = nx.Graph()
for i in range(len(newnode)):
    G2.add_node(newnode[i])

for p in range(0,len(to_list2)):
    G2.add_edges_from([(from_list2[p], to_list2[p])])

pos = nx.spring_layout(G2, k=0.5, iterations=100)
for n, p in pos.items():
    G2.nodes[n]['pos'] = p

edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#888'),
    hoverinfo='none',
    mode='lines')
for edge in G2.edges():
    x0, y0 = G2.nodes[edge[0]]['pos']
    x1, y1 = G2.nodes[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

#------------------------------------------------------------

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers+text',
    hoverinfo='text',
    marker=dict(
        showscale=False,
        colorscale='pinkyl',
        reversescale=False,
        color=[],
        size=37,
        line=dict(width=0)))
for node in G2.nodes():
    x, y = G2.nodes[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
for node, adjacencies in enumerate(G2.adjacency()):
    node_trace['marker']['color'] += tuple([len(adjacencies[1])])
    node_info = adjacencies[0]
    node_trace['text'] += tuple([node_info])

#--------------------------------------------------------------------------
# Outputting the required topology

title = "Least Weight path connecting "+str(pathends[0])+" and "+str(pathends[1])
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                title=title,
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=21, l=5, r=5, t=40),
                annotations=[dict(
                    text=" ",
                    showarrow=False,
                    xref="paper", yref="paper")],
                xaxis=dict(showgrid=False, zeroline=False,
                        showticklabels=False, mirror=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, mirror=False)))
fig.show()
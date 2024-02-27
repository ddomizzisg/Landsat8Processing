import networkx as nx #pip install networkx
import matplotlib.pyplot as plt #pip install matplotlib


"""
    A partir del objeto CFG del archivo de configuración CFG, se crea el grafo dirigido construido a partir de STAGES (definen fuentes -sources y salidas -sinks)
"""
def discover_workflow(cfg, workflow=None):
    discovered_workflow = nx.DiGraph() #create the Graph
    stages = cfg['STAGE'] #STAGES define the graph
    for stage in stages:
        source = stage['source'] #s in source : they're incoming edges to STAGE
        sink = stage['sink'] # si in sink : they're outgoing edges from STAGE
        if source.strip():
            sources = source.split(' ')
            for s in sources:
               discovered_workflow.add_edge(s, stage['name'], color='k')
        if sink.strip():
            sinks = sink.split(' ')
            for s in sinks:
               discovered_workflow.add_edge(stage['name'], s, color='k')
    
    if workflow is not None: #default workflow, add the edges 
        edges = workflow.edges
        for e in edges:
            if not discovered_workflow.has_edge(e[0], e[1]):
                discovered_workflow.add_edge(e[0], e[1], color='b')
    return discovered_workflow


"""
    Dado un grafo descubierto, la función genera el gráfico del grafo correspondiente
"""
def draw_workflow(G, output_path):
    #plt.clf()
    colors = nx.get_edge_attributes(G, 'color').values()
    graph_options = {
        'node_color': 'red',
        'edge_color': colors,
        #'font_color': 'brown',
        'node_size': 150,
        'width': 1,
        'arrowsize': 15,
        'font_size': 13,
        'with_labels': True
    }
    #nx.draw(G, **graph_options)
    #plt.margins(0.3)
    #plt.savefig(f"{output_path}/discovered_workflow.png")


    


"""
    Función de prueba, genera un grafo
"""
def create_workflow():
    G = nx.DiGraph()
    G.add_edge('@PWD/EServiceDicom/catalogs/UnaImagen', 'stage_cleaning', color='k')
    #G.add_edge('stage_preprocesing', 'stage_cleaning', color='k')
    G.add_edge('stage_cleaning', 'stage_dicomtojpg', color='k')
    G.add_edge('stage_cleaning', 'stage_x', color='k')
    #draw_workflow(G, 'reports/randomWF.png')
    return G
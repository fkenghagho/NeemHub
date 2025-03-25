from pyvis.network import Network
import networkx as nx
import time
import ipywidgets as widgets
from IPython.display import display, HTML,IFrame
import webbrowser




class NarrativeInspector():
    def __init__(self):
        self.symbols={'ACTION':['2.1.Locating','3.1.3.Grasping','4.1.TraceableInserting'],'OBJECT':['Canister_QUNRCLSD','CEA_GRIPPER_TEFHZXUW', 'DrainTray_PTYVBHGF'], 'PROPERTY':['Size_Canister_QUNRCLSD', 'Mesh_Canister_QUNRCLSD'], 'RELATION':['3.1.3.Grasping-Canister_QUNRCLSD', 'Canister_QUNRCLSD-DrainTray_PTYVBHGF', 'Canister_QUNRCLSD-CEA_GRIPPER_TEFHZXUW']}

        self.semantics_dict={
            '3.1.3.Grasping':{
                                'is_intance_of':'http://www.ease-crc.org/ont/SOMA.owl#Grasping',
                                'has_definition': 'A task in which an Agent uses its end effectors to grasp an object, thus gaining kinematic control over it.'
                            },
            'http://www.ease-crc.org/ont/SOMA.owl#Grasping':{
                            'has_role': 'AgentRole1',
                            'has_role': 'PatientRole2',
                            'has_verification_modality_distribution':'VerificationModalityDistribution',
                            'has_feasibility_influence': '0.3',
                            'has_parameter': 'GraspType',
                            'has_parameter': 'GraspEffort'
            },
            'VerificationModalityDistribution':{
                            'has_VMD': 'ModalityFactor1',
                            'has_VMD': 'ModalityFactor2',
                            'has_VMD': 'ModalityFactor3',
                            'has_VMD': 'ModalityFactor4'
            },
            'ModalityFactor1':{
                'has_modality':'OdometryModality',
                'has_capability': '0.3'
            },
            'ModalityFactor2':{
                'has_modality':'TactileModality',
                'has_capability': '0.35'
            }
            ,
            'ModalityFactor3':{
                'has_modality':'VisualModality',
                'has_capability': '0.15'
            },
            'ModalityFactor2':{
                'has_modality':'DTModality',
                'has_capability': '0.2'
            },
            'Canister_QUNRCLSD':{
                'has_color': 'Transparent',
                'has_color': 'Blue',
                'has_material': 'Glass',
                'has_size': 'Size_Canister_QUNRCLSD',
                'has_shape': 'Cylinder',
                'has_mesh': 'Mesh_Canister_QUNRCLSD',
                'is_subclass_of': 'TraceBot.Container'   
            },
            'Size_Canister_QUNRCLSD':{
                'has_diameter': '4.5cm',
                'has_height': '12.3cm'
            },
            'Mesh_Canister_QUNRCLSD':{
                'has_url':'https://github.com/fkenghagho/NeemHub/raw/refs/heads/main/TRACEBOT-NEEMS/Canister.obj',
                'display': True
            },
            'Canister_QUNRCLSD-CEA_GRIPPER_TEFHZXUW':{
                'involves': 'Canister_QUNRCLSD_1',
                'involves': 'CEA_GRIPPER_TEFHZXUW_1'   
            },
            'CEA_GRIPPER_TEFHZXUW_1':{
                'grasps': 'Canister_QUNRCLSD_1'
            },
            'Canister_QUNRCLSD-DrainTray_PTYVBHGF':{
                'involves': 'Canister_QUNRCLSD_1',
                'involves': 'DrainTray_PTYVBHGF_1'   
            },
            'DrainTray_PTYVBHGF_1':{
                'holds': 'Canister_QUNRCLSD_1'
            }
        }
        self.SELECTED_ITEM=''
        self.SELECTED_CATEGORY=''
        self.categoryW =None
        self.itemW =None
        self.icategoryW=None
        self.iitemW =None
        
    def update_ontology_frame(self, graph,initial_graph):
        red_color = "#FF7377"
        blue_color = "#87CEFB"
        nx_graph = nx.MultiDiGraph()
        seen_nodes=[]
        for k  in range(len(graph)):
            rel=graph[k].copy()
            if rel[0] not in seen_nodes:
                if rel[0].lower() in initial_graph:
                    nx_graph.add_node(rel[0], color=blue_color)
                else:
                    nx_graph.add_node(rel[0], color=red_color)

                if rel[2] not in seen_nodes:
                    if rel[2].lower() in initial_graph:
                        nx_graph.add_node(rel[2], color=blue_color)
                    else:
                        nx_graph.add_node(rel[2], color=red_color)
            if rel[1].lower() in initial_graph:
                nx_graph.add_edge(rel[0], rel[2], color=blue_color, label=rel[1])
            else:
                nx_graph.add_edge(rel[0], rel[2], color=red_color, label=rel[1])
            #time.sleep(0.1)
            nt = Network('100%', '100%', directed=True)
            nt.from_nx(nx_graph)
            nt.set_options("""
                                                            const options = {
                                                              "physics": {
                                                                "enabled": true,
                                                                "barnesHut": {
                                                                  "gravitationalConstant": -4200,
                                                                  "centralGravity": 0.95,
                                                                  "springLength": 130,
                                                                  "springConstant": 0.015,
                                                                  "damping": 0.01,
                                                                  "overlap":1.0
                                                                },
                                                                "maxVelocity": 5,
                                                                "minVelocity": 0.0001
                                                              }
                                                            }
                                                            """)
            if nt is not None:
                if k <len(graph)-1:
                    nt.options['physics']['enabled'] = False
                else:
                    nt.options['physics']['enabled'] = True
            self.graphText = nt.generate_html()
            self.graphText = self.graphText.replace('<div class="card" style="width: 100%">', '<div class="card" style="width: 100%;height: 100%">')
            f = open("nx.html", "w")
            #print(self.graphText)
            f.write(self.graphText)
            f.close()
        return True
    
    def build_graph(self, symbol):
        if symbol in list(self.semantics_dict.keys()):
            actual_result=[]
            for key in self.semantics_dict[symbol].keys():
                actual_result.append([symbol, key, self.semantics_dict[symbol][key]])
                actual_result=actual_result+self.build_graph(self.semantics_dict[symbol][key])
            return actual_result
        else:
            return []
        
    def show(self):
        display(IFrame('nx.html', width=1000, height=700))
        
    def load(self):
        self.update_ontology_frame(self.build_graph(self.SELECTED_ITEM),[])
        self.show()

    def generate_options(self):
    
        self.categoryW = widgets.Dropdown(options=self.symbols.keys())
        init_category = self.categoryW.value
        self.itemW = widgets.Dropdown(options=self.symbols[init_category])
        
        self.icategoryW = widgets.interactive(self.select_item, category=self.categoryW)
        self.iitemW = widgets.interactive(self.get_item, item=self.itemW)
        
        display(self.icategoryW)
        display(self.iitemW)
        
        self.button_inspect = widgets.Button(description = 'Inspect')   
        self.button_inspect.on_click(self.clicked)
        display(self.button_inspect)
        

    def clicked(self,arg):
        print(str(arg))
        self.load()
        #self.show()

    def get_item(self,item):
        self.SELECTED_ITEM=item
        print(self.SELECTED_ITEM)

    def select_item(self,category):
        self.SELECTED_CATEGORY=category
        self.itemW.options = self.symbols[category]

    

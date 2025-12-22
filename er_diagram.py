import matplotlib.pyplot as plt
import networkx as nx
G=nx.DiGraph()
G.add_edges_from([('drivers','vehicles'),('vehicles','charging_sessions'),('tariffs','charging_sessions')])
pos=nx.spring_layout(G, seed=1)
plt.figure(figsize=(6,4))
nx.draw(G,pos,with_labels=True,node_color='#3a86ff',node_size=3000,font_size=12,font_color='white',arrows=True)
plt.title('EV-HCRM ER Diagram')
plt.tight_layout()
plt.savefig('er_diagram.png')
print('er_diagram.png created ✅')

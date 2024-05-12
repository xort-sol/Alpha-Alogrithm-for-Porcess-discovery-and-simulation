import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def preprocess_event_log(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Display the event log
    print("Event Log:")
    # print(df)
    print()
    
    # Preprocess the event log to generate `multi-set of traces L
    traces = df.groupby('TicketNum')['Status'].apply(list).tolist()
    # print("Multi-set of traces L:")
    # for i, trace in enumerate(traces, start=1):
    #     print(f"Trace {i}: {trace}")
    # print()
    
    return traces

def identify_tl(traces):
    # Identify and display set TL (distinct activities)
    tl = set()
    for trace in traces:
        tl.update(trace)
    # print("Set TL (Distinct Activities):", tl)
    print()
    
    return tl

def identify_ti_to(tl, traces):
    # Identify start (TI) and end (TO) events
    ti = set(trace[0] for trace in traces)
    to = set(trace[-1] for trace in traces)
    # print("Start Events (TI):", ti)
    # print("End Events (TO):", to)
    # print()
    
    return ti, to

def identify_pl_fl(tl, traces):
    # Identify set PL (successor activities) and FL (predecessor activities)
    pl = {}
    fl = {}
    for activity in tl:
        pl[activity] = set()
        fl[activity] = set()
    
    for trace in traces:
        for i in range(len(trace) - 1):
            pl[trace[i]].add(trace[i + 1])
            fl[trace[i + 1]].add(trace[i])
    
    # print("Set PL (Successor Activities):", pl)
    # print("Set FL (Predecessor Activities):", fl)
    # print()
    
    return pl, fl

def visualize_process(tl, pl, fl):
    # Create a directed graph for visualization
    G = nx.DiGraph()
    
    # Add nodes for TL
    G.add_nodes_from(tl)
    
    # Add edges for PL
    for activity, successors in pl.items():
        for successor in successors:
            G.add_edge(activity, successor)
    
    # Create a color palette for arrows
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    
    # Visualize the graph with custom layout and arrow positions
    plt.figure(figsize=(12, 8))
    
    # Position nodes in a circular layout
    pos = nx.circular_layout(G, scale=2)  # Increase the scale to push nodes to outer boundary
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=0, node_color='lightblue')
    
    # Draw edges with arrows in the middle
    for i, (node1, node2) in enumerate(G.edges()):
        x1, y1 = pos[node1]
        x2, y2 = pos[node2]
        dx, dy = x2 - x1, y2 - y1
        edge_color = colors[i % len(colors)]  # Cycle through colors for edges
        nx.draw_networkx_edges(G, pos, edgelist=[(node1, node2)], arrows=False, width=1.0, edge_color=edge_color)
        plt.arrow(x1, y1, dx * 0.5, dy * 0.5, head_width=0.05, head_length=0.1, fc=edge_color, ec=edge_color)
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    
    plt.title("Discovered Process Visualization")
    plt.axis('off')
    plt.show()


def simulate_execution(traces, tl, pl):
    # Simulate execution of each trace on the discovered process
    print("Simulation of Trace Execution on Discovered Process:")
    for i, trace in enumerate(traces, start=1):
        print(f"Trace {i}:")
        current_activity = trace[0]
        print(f"Start: {current_activity}")
        for activity in trace[1:]:
            if activity not in pl[current_activity]:
                print(f"Error: {current_activity} cannot lead to {activity}")
                break
            print(f"{current_activity} -> {activity}")
            current_activity = activity
        if current_activity != trace[-1]:
            print("Error: Trace not completed")
        print()

# Main function
def main():
    # Path to the Excel file containing event log
    file_path = "AnonymizedEventData.xlsx"
    
    # Step 1: Preprocessing the event log
    traces = preprocess_event_log(file_path)
    
    # Step 2: Identifying and displaying TL
    tl = identify_tl(traces)
    
    # Step 3: Identifying and displaying TI and TO
    ti, to = identify_ti_to(tl, traces)
    
    # Step 4 & 5: Identifying and displaying PL and FL
    pl, fl = identify_pl_fl(tl, traces)
    
    # Extra Credit: Visualize the discovered process
    visualize_process(tl, pl, fl)
    
    # Step 6: Outputting the resultant process
    print("Resultant Process:")
    print("--------------------------------")
    print("TL: 1")
    print("TI: 2")
    print("TO: 3")
    print("PL: 4")
    print("FL: 5")
    print("exit: 6")
    print("--------------------------------")
    option = 0
    while(option < 7 ):

        print("Enter option: ")
        option = int(input())
        if(option == 1):
            print("TL: ", tl)
        elif(option == 2):
            print("TI: ", ti)
        elif(option == 3):
            print("TO: ", to)
        elif(option == 4):
            print("PL: ", pl)
        elif(option == 5):
            print("FL: ",fl)
        elif(option == 6):
            simulate_execution(traces, tl, pl)
        else:
            print("Invalid option")
            print("--------------------------------")
            print("TL: 1")
            print("TI: 2")
            print("TO: 3")
            print("PL: 4")
            print("FL: 5")
            print("Simulate execution of each trace on the discovered process: 6 ")
            print("exit: 7")
            print("--------------------------------")
            option = 0



  
    # Part B: Simulate execution of each trace on the discovered process
   

if __name__ == "__main__":
    main()
 # type: ignore
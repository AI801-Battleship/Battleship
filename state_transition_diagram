from graphviz import Digraph

def create_state_transition_diagram():
    dot = Digraph()
    
    # Define nodes
    dot.node('Start', 'Initial State')
    dot.node('Generate_1', 'Generate Random Guess')
    dot.node('Check_Guess', 'Check Guess')
    dot.node('Action', 'Action')
    dot.node('Max', 'Maximum Value from Q-Table')
    dot.node('Reward','Calculate Reward from action S1 to S2')
    dot.node('Update_Q', 'Update Q-Table Values')
    
    dot.attr(rankdir='TB')  # Top to Bottom layout

    # Define edges
    dot.edge('Start','Generate_1', label='Epsilon')
    dot.edge('Generate_1', 'Check_Guess')
    dot.edge('Check_Guess', 'Action')
    dot.edge('Check_Guess', 'Generate_1', style='dotted')
    dot.edge('Start','Max')
    dot.edge('Max','Action')
    dot.edge('Action','Reward')
    dot.edge('Reward','Update_Q')
    dot.edge('Update_Q','Start')
    
    
    #If you want certain nodes to be on the same level in the graph you can manually define them. ie targeting and exploratory are on the same level
    # with dot.subgraph() as s:
    #     s.attr(rank='same')
    #     s.node('Valid_Guess')
    # with dot.subgraph() as s:
    #     s.attr(rank='same')
    #     s.node('Targeting_Behavior')
    #     s.node('Exploratory_Behavior')
    # Render the graph
    dot.render('state_transition_diagram', format='png', view=True)

create_state_transition_diagram()

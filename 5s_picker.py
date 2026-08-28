import random
import streamlit as st
import networkx as nx

# streamlit page config
st.set_page_config(page_title="5S Teams", page_icon=":material/cleaning:", layout="centered")

st.title("5S Teams")
st.write("This app generates randomized teams for weekly 5S.")

st.sidebar.header("Settings")
names_input = st.sidebar.text_area("Enter names (one per line):", value="Justin\nKim\nSerena\nJacob\nLeia\nBing\nFrancisco")
exclusions_input = st.sidebar.text_area("Enter exclusions (one per line, format: name1,name2):", value="Justin,Francisco")
num_teams = st.sidebar.number_input("Number of teams:", min_value=1, max_value=10, value=2, step=1)

# FIX 1: Changed 'names.split' to 'names_input.split'
members = [name.strip() for name in names_input.split("\n") if name.strip()]

exclusions = []
for line in exclusions_input.split("\n"):
    if "," in line:
        p1, p2 = [p.strip() for p in line.split(",")]
        if p1 in members and p2 in members:
            exclusions.append((p1, p2))

def generate_teams(members, exclusions, num_teams):
    shuffled_members = list(members)
    random.shuffle(shuffled_members)
    
    teams = {i: [] for i in range(num_teams)}
    
    G = nx.Graph()
    G.add_nodes_from(shuffled_members)
    G.add_edges_from(exclusions)
    
    for member in shuffled_members:
        sorted_teams = sorted(teams.keys(), key=lambda t: len(teams[t]))
        assigned = False
        for team_idx in sorted_teams:
            has_conflict = any(G.has_edge(member, teammate) for teammate in teams[team_idx])
            if not has_conflict:
                teams[team_idx].append(member)
                assigned = True
                break
        if not assigned:
            teams[sorted_teams[0]].append(member)
            
    return teams

if st.button("🔀 Generate Teams", type="primary"):
    if len(members) < num_teams:
        st.error("You have more teams than total people! Please add more names.")
    else:
        with st.spinner("Calculating perfect teams..."):
            # FIX 2: Fixed the argument order to match the function definition
            final_teams = generate_teams(members, exclusions, num_teams)
            
        st.success("Teams generated successfully!")
        
        # Display teams in a clean grid layout
        cols = st.columns(num_teams)
        for idx, col in enumerate(cols):
            with col:
                st.subheader(f":material/cleaning_services: Team {idx + 1}")
                for teammate in final_teams[idx]:
                    st.markdown(f"• **{teammate}**")

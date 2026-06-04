"""
TOPS Technologies - Agentic AI Assessment
Title: Autonomous Supply Chain Disruptor Mitigation Agent

Author: Your Name
"""

# =====================================================
# IMPORTS
# =====================================================

import pandas as pd
import yaml
import sqlite3
import requests
from typing import TypedDict

from sqlalchemy import create_engine

from langgraph.graph import StateGraph, END

# =====================================================
# SECTION A ANSWERS
# =====================================================

section_a_answers = {

    "Q1":
    "Agentic AI possesses autonomy and can make decisions and take actions toward goals without requiring human prompts at every step.",

    "Q2":
    "Autonomy",

    "Q3":
    "Recommendation systems only generate predictions and do not independently execute actions toward goals.",

    "Q4":
    "Reactive agents respond to environmental changes. Proactive agents initiate actions to achieve future goals.",

    "Q5":
    "Agentic AI extends LLMs by adding planning, memory, reasoning, tool use and autonomous execution."
}

# =====================================================
# DATABASE SETUP
# =====================================================

engine = create_engine("sqlite:///shipments.db")

# Sample Data
shipment_df = pd.DataFrame({

    "ShipmentID":[1,2,3,4],

    "Route":[
        "Asia-Europe",
        "Asia-USA",
        "India-Europe",
        "India-USA"
    ],

    "DelayDays":[12,1,8,0],

    "Cost":[2000,2500,1800,2100]
})

shipment_df.to_sql(
    "shipments",
    engine,
    if_exists="replace",
    index=False
)

# =====================================================
# TOOL 1 : SQL TOOL
# =====================================================

def sql_tool(query:str):

    conn = sqlite3.connect("shipments.db")

    result = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return result.to_string()


# =====================================================
# TOOL 2 : WEB SEARCH TOOL
# =====================================================

def web_search_tool(query):

    try:

        url = f"https://api.duckduckgo.com/?q={query}&format=json"

        response = requests.get(url)

        return response.json().get(
            "Abstract",
            "No web result found"
        )

    except:

        return "Search failed"


# =====================================================
# REACT STYLE TOOL ROUTER
# =====================================================

def react_agent(user_query):

    sql_keywords = [
        "shipment",
        "delay",
        "route",
        "database",
        "cost"
    ]

    if any(
        word in user_query.lower()
        for word in sql_keywords
    ):

        return sql_tool(
            "SELECT * FROM shipments"
        )

    else:

        return web_search_tool(
            user_query
        )


# =====================================================
# LANGGRAPH AGENT
# =====================================================

class AgentState(TypedDict):

    shipment_id:int

    delay:int

    action:str

    status:str


# =====================================================
# NODE 1
# =====================================================

def detect_bottleneck(state):

    if state["delay"] > 7:

        state["action"] = \
            "Bottleneck Detected"

    else:

        state["action"] = \
            "Normal"

    return state


# =====================================================
# NODE 2
# =====================================================

def propose_alternative(state):

    if state["action"] == \
            "Bottleneck Detected":

        state["action"] = \
            "Use Alternative Route"

    return state


# =====================================================
# NODE 3
# =====================================================

def negotiate(state):

    if state["action"] == \
            "Use Alternative Route":

        state["status"] = \
            "Negotiated New Route"

    return state


# =====================================================
# ERROR CORRECTION NODE
# =====================================================

def error_checker(state):

    if state["status"] == "":

        state["status"] = \
            "Retry"

    return state


# =====================================================
# BUILD LANGGRAPH
# =====================================================

workflow = StateGraph(AgentState)

workflow.add_node(
    "detect",
    detect_bottleneck
)

workflow.add_node(
    "alternative",
    propose_alternative
)

workflow.add_node(
    "negotiate",
    negotiate
)

workflow.add_node(
    "error_check",
    error_checker
)

workflow.set_entry_point("detect")

workflow.add_edge(
    "detect",
    "alternative"
)

workflow.add_edge(
    "alternative",
    "negotiate"
)

workflow.add_edge(
    "negotiate",
    "error_check"
)

workflow.add_edge(
    "error_check",
    END
)

graph = workflow.compile()

# =====================================================
# YAML CONFIG
# =====================================================

autogpt_yaml = """

agent:
  name: MarketResearchAgent

objective:
  - Analyze shipping delays
  - Find alternate routes
  - Estimate cost impact
  - Generate report

constraints:
  - Budget under 10%
  - Delay under 5 days
  - No human intervention

memory:
  backend: local
  persistence: true
  path: ./memory/

"""

yaml_config = yaml.safe_load(
    autogpt_yaml
)

# =====================================================
# RULE BASED WORKFLOW
# =====================================================

def rule_based_agent(delay):

    if delay > 10:

        return \
            "Alternative Route"

    else:

        return \
            "No Action"


# =====================================================
# SEMANTIC STYLE AGENT
# =====================================================

def semantic_agent(delay):

    reasoning = []

    if delay > 7:

        reasoning.append(
            "Detected risk"
        )

        reasoning.append(
            "Search alternatives"
        )

        reasoning.append(
            "Negotiate route"
        )

        reasoning.append(
            "Update logistics"
        )

    return reasoning


# =====================================================
# COMPARISON
# =====================================================

def compare_agents():

    delay = 12

    rule = rule_based_agent(delay)

    semantic = semantic_agent(delay)

    print("\nRULE BASED")

    print(rule)

    print("\nAGENTIC")

    print(semantic)

    print(
        "\nAutonomy Score:"
    )

    print(
        f"Rule Based Steps: 1"
    )

    print(
        f"Agentic Steps: {len(semantic)}"
    )


# =====================================================
# MINI PROJECT EXECUTION
# =====================================================

def run_supply_chain_agent():

    print(
        "\nAUTONOMOUS SUPPLY CHAIN AGENT\n"
    )

    shipment_data = shipment_df

    for _, row in shipment_data.iterrows():

        state = {

            "shipment_id":
            row["ShipmentID"],

            "delay":
            row["DelayDays"],

            "action":"",

            "status":""
        }

        result = graph.invoke(state)

        print(result)


# =====================================================
# SYSTEM ARCHITECTURE
# =====================================================

architecture = """

DATASET
   |
   v
Bottleneck Detector
   |
   v
Planner Agent
   |
   v
Route Negotiation Agent
   |
   v
Error Correction Agent
   |
   v
Final Decision

"""


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("\nSECTION A ANSWERS\n")

    for k,v in section_a_answers.items():

        print(k,":",v)

    print("\nSYSTEM ARCHITECTURE")

    print(architecture)

    print("\nTOOL CALL DEMO")

    print(
        react_agent(
            "show shipment delays"
        )
    )

    compare_agents()

    run_supply_chain_agent()

    print("\nYAML CONFIG")

    print(
        yaml.dump(
            yaml_config,
            sort_keys=False
        )
    )

    print(
        "\nPROJECT COMPLETED"
    )


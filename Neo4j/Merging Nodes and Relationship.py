'''
MERGE (n1:node {name:'Adam'})
MERGE (n2:node {name:'USA'})
MERGE (n1)-[r:born_in]->(n2)
'''
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

'''
What is the use of MERGE ?
MERGE is a shortcut for creating a node and connecting it to an existing node.
If the node already exists, the MERGE will simply connect the node to the existing node.
If the node does not exist, the MERGE will create a new node and connect it to the existing node.
'''

def merge_nodes(tx, name):
    tx.run("MERGE (n1:node {name:$name})", name=name)

def merge_relationship(tx, name, country):
    tx.run("MERGE (n1:Person {name:$name})-[r:born_in]->(n2:Country {name:$country})", name=name, country=country)

with driver.session() as session:
    # session.write_transaction(merge_nodes, "Adam")
    # session.write_transaction(merge_nodes, "USA")
    session.write_transaction(merge_relationship, "Adam", "USA")

driver.close()
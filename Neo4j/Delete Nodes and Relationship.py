from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

# Delete the node with the given name
def delete_node(tx, name):
    tx.run("MATCH (a:Person) WHERE a.name = $name "
           "DETACH DELETE a", name=name)

def delete_particular_relationship(tx, name, friend):
    tx.run("MATCH (a:Person)-[r]->(b:Person) WHERE a.name = $name AND b.name = $friend "
           "DETACH DELETE r", name=name, friend=friend)

def delete_all_relationships(tx, name):
    tx.run("MATCH (a:Person)-[r]->(b:Person) WHERE a.name = $name "
           "DETACH DELETE r", name=name)

def delete_all_nodes(tx):
    tx.run("MATCH (n) DETACH DELETE n")

with driver.session() as session:
    # session.write_transaction(delete_particular_relationship, "Alice", "Bob")
    # session.write_transaction(delete_all_relationships, "Alice")
    # session.write_transaction(delete_node, "Alice")
    session.write_transaction(delete_all_nodes)

driver.close()
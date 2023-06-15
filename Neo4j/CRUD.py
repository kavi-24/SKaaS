from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def create_person(tx, name):
    tx.run("CREATE (a:Person {name: $name}) RETURN a", name=name)

def create_relation(tx, name, friend):
    tx.run("MATCH (a:Person {name: $name}), (b:Person {name: $friend}) CREATE (a)-[:KNOWS]->(b)", name=name, friend=friend)

def display_all_data(tx):
    for record in tx.run("MATCH (a) RETURN a"):
        print(record)

def change_name(tx, oldname, newname):
    tx.run("MATCH (a:Person {name: $oldname}) SET a.name = $newname", oldname=oldname, newname=newname)

def delete_all_data(tx):
    tx.run("MATCH (a) DETACH DELETE a")

with driver.session() as session:
    session.run("CREATE (a:Person {name: 'Arthur'})")
    session.write_transaction(create_person, "Bob")
    session.write_transaction(create_relation, "Arthur", "Bob")
    session.read_transaction(display_all_data)
    session.write_transaction(change_name, "Bob", "Robert")
    session.read_transaction(display_all_data)
    session.write_transaction(delete_all_data)

driver.close()
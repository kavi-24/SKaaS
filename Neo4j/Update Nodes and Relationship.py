from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))


def update_person(tx, oldname, newname):
    tx.run("MATCH (a:Person) WHERE a.name = $oldname "
           "SET a.name = $newname", oldname=oldname, newname=newname)


with driver.session() as session:
    session.write_transaction(update_person, "Alice", "Alice in Wonderland")

driver.close()
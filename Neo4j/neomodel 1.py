from neomodel import config, StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo

'''
from neomodel import db
db.set_connection('bolt://neo4j:neo4j@localhost:7687')
'''
config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'


class Country(StructuredNode):
    code = StringProperty(unique_index=True, required=True)


class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)

    # traverse outgoing IS_FROM relations, inflate to Country objects
    country = RelationshipTo(Country, 'IS_FROM')

jim = Person(name="Jim", age="3").save()  # Must save to return the object
jim.age = 4
jim.save()  # Update, if valid changes
# p1.delete()
jim.refresh()  # # reload properties from the database
print(jim.id)

# Return all nodes
all_nodes = Person.nodes.all()
# Returns Person by Person.name or raises neomodel.DoesNotExist if no match
result = Person.nodes.get(name='Jim')

'''
.nodes.all() and .nodes.get() can also accept a lazy=True parameter which will result in those functions simply returning the node IDs rather than every attribute associated with that Node.
'''

# Will return None unless "bob" exists
someone = Person.nodes.get_or_none(name='bob')
# Will return the first Person node with the name bob. This raises neomodel.DoesNotExist if there's no match.
someone = Person.nodes.first(name='bob')
# Will return the first Person node with the name bob or None if there's no match
someone = Person.nodes.first_or_none(name='bob')
# Return set of nodes
people = Person.nodes.filter(age__gt=3)


germany = Country(code='DE').save()
jim.country.connect(germany)

if jim.country.is_connected(germany):
    print("Jim's from Germany")
for p in germany.inhabitant.all():
    print(p.name) # Jim

print(len(germany.inhabitant)) # 1

# Find people called 'Jim' in germany
germany.inhabitant.search(name='Jim')

# Find all the people called in germany except 'Jim'
germany.inhabitant.exclude(name='Jim')

# Remove Jim's country relationship with Germany
jim.country.disconnect(germany)

usa = Country(code='US').save()
jim.country.connect(usa)
jim.country.connect(germany)

# Remove all of Jim's country relationships
jim.country.disconnect_all()

jim.country.connect(usa)
# Replace Jim's country relationship with a new one
jim.country.replace(germany)

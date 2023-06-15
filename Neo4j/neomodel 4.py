from neomodel import StructuredRel, DateTimeProperty, StructuredNode, StringProperty, RelationshipTo, config
from datetime import datetime
from pendulum import yesterday
import pytz

config.DATABASE_URL = "bolt://neo4j:password@localhost:7687"

class FriendRel(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.now(pytz.utc)
    )
    met = StringProperty()

class Person(StructuredNode):
    name = StringProperty()
    friends = RelationshipTo('Person', 'FRIEND', model=FriendRel)

jim = Person(name="Jim").save()
bob = Person(name="Bob").save()


rel = jim.friends.connect(bob)
print(rel.since) # datetime object

rel = jim.friends.connect(bob, {'since': yesterday, 'met': 'Paris'})

print(rel.start_node().name) # jim
print(rel.end_node().name) # bob

rel.met = "Amsterdam"
rel.save()

'''
You can retrieve relationships between two nodes using the 'relationship' method. This is only available for relationships with a defined relationship mode
'''
rel = jim.friends.relationship(bob)
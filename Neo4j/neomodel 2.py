from datetime import datetime
import pytz

from neomodel import config, StructuredNode, StringProperty, RelationshipTo, RelationshipFrom
# Importing constants One, Two, ZeroOrOne, ZeroOrMany, etc.
from neomodel.cardinality import *
from neomodel.relationship import StructuredRel
from neomodel.properties import DateTimeProperty

config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

# class Person(StructuredNode):
#     friends = Relationship('Person', 'FRIEND')

# class Garage(StructuredNode):
#     cars = RelationshipTo('transport.models.Car', 'CAR')
#     vans = RelationshipTo('.models.Van', 'VAN')

'''
It is possible to (softly) enforce cardinality constraints on your relationships. Remember this needs to be declared on both sides of the relationship definition:
'''

class Person(StructuredNode):
    car = RelationshipTo('Car', 'OWNS', cardinality=One)


class Car(StructuredNode):
    owner = RelationshipFrom('Person', 'OWNS', cardinality=One)


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
rel.since  # datetime object

rel = jim.friends.connect(bob,
                          {'since': 'yesterday', 'met': 'Paris'})

print(rel.start_node().name) # jim
print(rel.end_node().name) # bob

rel.met = "Amsterdam"
rel.save()

# You can retrieve relationships between two nodes using the ‘relationship’ method. This is only available for relationships with a defined relationship model:

rel = jim.friends.relationship(bob)
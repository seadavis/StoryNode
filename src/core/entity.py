
"""
Class for holding and accessing a
"Named Entity" for a relation
"""
class NamedEntity:

    def __init__(self, entity, doc):
        self.entity = entity
    
    """
    Gets the type of entity
    this object represents.

    "PERSON", "ORG", etc.
    """
    @property
    def entity_type(self):
        return None

    """
    Gets the text span of this entity,
    referring to the original document
    """
    @property
    def text(self):
        return None


"""
Holds a set of entities, not necessarily from the same collection

This is an immutable collection
"""
class NamedEntityCollection:

    def __init__(self, entities):
        self.entities = self.entities

    def join(self, other):
        return []

    def get_entity(self, span):
        return None

    def get_entityies_by_type(self, type):
        return None

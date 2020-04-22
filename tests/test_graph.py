from pygds import GDS

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "admin")


def test_gds_enter():    
    with GDS(URI, auth=AUTH):
        pass


def test_create_and_drop_graph():
    with GDS(URI, auth=AUTH) as gds:
        gds.graph.create("graph", "*", "*")
        gds.graph.drop("graph")

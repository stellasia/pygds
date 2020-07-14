import pytest
from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
from pygds import GDS
from . import URI, AUTH


def setup_module():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        session.run("""
        CREATE (:Node)-[:REL]->(:Node)
        """)


def test_create_graph_with_dict_projections():
    with GDS(URI, auth=AUTH) as gds:
        gds.graph.create("graph", {"Node": {"label": "Node"}}, {"REL": {"type": "REL", "orientation": "UNDIRECTED"}})
        gds.graph.drop("graph")


def test_create_and_drop_graph():
    with GDS(URI, auth=AUTH) as gds:
        gds.graph.create("graph", "*", "*")
        gds.graph.drop("graph")


def test_create_existing_graph():
    with GDS(URI, auth=AUTH) as gds:
        gds.graph.create("graph", "*", "*")
        with pytest.raises(ClientError):
            gds.graph.create("graph", "*", "*")
        gds.graph.drop("graph")


def teardown_module():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        session.run("""
        MATCH (n) DETACH DELETE n
        """)
    with GDS(URI, auth=AUTH) as gds:
        try:
            gds.drop("graph")
        except:
            pass

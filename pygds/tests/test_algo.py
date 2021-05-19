import pytest
from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
from pygds import GDS
from . import URI, AUTH


def setup_module():
    print(URI, AUTH)
    driver = GraphDatabase.driver(URI, auth=AUTH, encrypted=False)
    with driver.session() as session:
        session.run("""
        CREATE (:Node)-[:REL]->(:Node)
        """)
    with GDS(URI, auth=AUTH, encrypted=False) as gds:
        gds.graph.create("graph", "*", "*")


def test_algo_stream_on_named_projected_graph():
    with GDS(URI, auth=AUTH, encrypted=False) as gds:
        pr = gds.pageRank.stream("graph", {})
    assert pr is not None
    assert len(pr) == 2
    assert "nodeId" in pr[0] and "score" in pr[0]


def test_algo_stream_on_anonymous_projected_graph():
    with GDS(URI, auth=AUTH, encrypted=False) as gds:
        pr = gds.pageRank.stream({"nodeProjection": "*", "relationshipProjection": "*"})
    assert pr is not None
    assert len(pr) == 2
    assert "nodeId" in pr[0] and "score" in pr[0]
    assert pr[0]["score"] is not None


def test_wrong_algo_name():
    with GDS(URI, auth=AUTH, encrypted=False) as gds:
        with pytest.raises(ClientError):
            gds.some_non_existing_procedure()

        with pytest.raises(AttributeError):
            gds.graph.some_non_exising_procedure()


def teardown_module():
    with GDS(URI, auth=AUTH, encrypted=False) as gds:
        gds.graph.drop("graph")
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        session.run("""
        MATCH (n) DETACH DELETE n
        """)

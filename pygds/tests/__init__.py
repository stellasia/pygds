import os
from pygds import GDS

URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
AUTH = (
    os.environ.get("NEO4J_USER", "neo4j"),
    os.environ.get("NEO4J_PASSWORD", "----"),
    # "neo4j", "PyGdsNeo4jPassword"
)


def test_gds_enter():
    with GDS(URI, auth=AUTH):
        pass

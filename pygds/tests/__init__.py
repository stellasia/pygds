import os
from pygds import GDS

URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
AUTH = (
    os.environ.get("NEO4J_USER", "neo4j"),
    os.environ.get("NEO4J_PASSWORD", "----"),
)


def test_gds_enter():
    print(URI, AUTH)
    with GDS(URI, auth=AUTH):
        pass

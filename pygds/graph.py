from .mixins import Neo4jRunner


class GraphCreate(Neo4jRunner):
    """Create a named projected graph through
    natitve (__call__) or cypher projection.
    """

    def __init__(self, driver, namespace):
        super().__init__()
        self.namespace = namespace
        self.driver = driver

    def __call__(self, graph_name, node_projection="*", relationship_projection="*"):
        """Create a projected graph from native projection
        """
        cypher = "CALL gds.graph.create($graph_name, $node_projection, $relationship_projection)"
        return self.run_cypher(cypher, {
            "graph_name": graph_name,
            "node_projection": node_projection,
            "relationship_projection": relationship_projection
        })

    def cypher(self, graph_name, node_projection, relationship_projection):
        """Create a projected graph from Cypher projection
        """
        cypher = "CALL gds.graph.create.cypher($graph_name, $node_projection, $relationship_projection)"
        return self.run_cypher(cypher, {
            "graph_name": graph_name,
            "node_projection": node_projection,
            "relationship_projection": relationship_projection
        })


class Graph(Neo4jRunner):
    """Class to manage named projected graph
    """

    def __init__(self, driver, namespace):
        super().__init__()
        self.namespace = namespace
        self.driver = driver

    @property
    def create(self, *args, **kwargs):
        return GraphCreate(self.driver, self.namespace, *args, **kwargs)

    def list(self, name=""):
        cypher = "CALL gds.graph.list($name)"
        return self.run_cypher(cypher, {"name": name})

    def exists(self, name=None):
        cypher = "CALL gds.graph.exists($name)"
        return self.run_cypher(cypher, {"name": name})

    def drop(self, graph_name):
        """Drop an existing projected graph
        """
        cypher = "CALL gds.graph.drop($graph_name)"
        return self.run_cypher(cypher, {
            "graph_name": graph_name,
        })

    def export(self, graph_name, config):
        cypher = "CALL gds.graph.export($graph_name, $config)"
        return self.run_cypher(
            cypher,
            {
                "graph_name": graph_name,
                "config": config
            }
        )

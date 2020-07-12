from neo4j import GraphDatabase
from .graph import Graph
from .algorithms import (
    AlgoWrite,
    AlgoStream,
    AlgoMutate,
    AlgoStats,
    Function
)


class ItemGetter:
    """
    This class is the core of the library, which allows to use
    the same syntax as the Cypher procedures:
    - gds.louvain.write(...)
    - gds.louvain.stream(...)
    - gds.louvain.stats(...)
    - gds.alpha.betweenness.stream(...)
    - gds.alpha.similarity.euclideanSimilarity(...)
    - etc...

    Basically, this class implements the "end" functions (write, stream, stats and __call__)
    If trying to access any other attribute such as "louvain", the  __getattr__ method
    will just append the attribute name to the `namespace` and return another instance
    of ItemGetter.

    It means that:
    - gds.louvain => returns an ItemGetter instance wtih namespace `gds.louvain`
    - gds.louvain() => returns an Function instance wtih namespace `gds.louvain`
        (from the __call__ method of ItemGetter)
    - gds.louvain.write => returns an AlgoWritter instance wtih namespace `gds.louvain`

    The actual execution of the algorithm is performed in the Algo class.
    """

    def __init__(self, driver, namespace=None):
        self.driver = driver
        self.namespace = namespace

    def __call__(self, *args, **kwargs):
        return Function(self.driver, self.namespace)(*args, **kwargs)

    @property
    def graph(self, *args, **kwargs):
        return Graph(self.driver, self.namespace)

    @property
    def write(self, *args, **kwargs):
        return AlgoWrite(self.driver, self.namespace)

    @property
    def stream(self, *args, **kwargs):
        return AlgoStream(self.driver, self.namespace)

    @property
    def mutate(self, *args, **kwargs):
        return AlgoMutate(self.driver, self.namespace)

    @property
    def stats(self, *args, **kwargs):
        return AlgoStats(self.driver, self.namespace)

    def __getattr__(self, attr):
        namespace = ".".join([self.namespace, attr])
        return ItemGetter(self.driver, namespace)


class GDS:

    # all procedures from the GDS are under the "gds" namespace
    namespace = "gds"

    def __init__(self, uri, auth):
        """
        The main public class for this package

        Parameters are connection parameters to the Neo4j graph,
        similar to the Neo4j python driver:

        :param str uri:
        :param tuple auth:
        """
        self.uri = uri
        self.auth = auth
        self.driver = GraphDatabase.driver(self.uri, auth=self.auth)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.driver.close()

    def __del__(self):
        try:
            self.driver.close()
        except Exception:
            pass

    def __getattr__(self, attr):
        return getattr(ItemGetter(self.driver, self.namespace), attr)

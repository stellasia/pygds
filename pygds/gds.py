from neo4j import GraphDatabase
from .graph import Graph
from .algorithms import (
    AlgoWrite,
    AlgoStream,
    AlgoStats,
    Function
)


class ItemGetter:

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
    def stats(self, *args, **kwargs):
        return AlgoStats(self.driver, self.namespace)

    def __getattr__(self, attr):
        namespace = ".".join([self.namespace, attr])
        return ItemGetter(self.driver, namespace)


class GDS:

    namespace = "gds"

    def __init__(self, uri, auth):
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

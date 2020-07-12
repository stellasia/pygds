from .mixins import Neo4jRunner


class Function(Neo4jRunner):

    def __init__(self, driver, namespace):
        super().__init__()
        self.namespace = namespace
        self.driver = driver

    def __call__(self, *args):
        """Run algorithm and write results back into Neo4j
        Returns some stats about algorithm execution
        """
        func_name = self.namespace
        params = {str(k): a for k, a in enumerate(args)}
        params_names = params.keys()
        cypher = f"RETURN {func_name}($" + ", $".join(params_names) + ") as result"
        return self.run_cypher(cypher, params, get_data=False).single().get("result")


class AlgoMixin(Neo4jRunner):
    """Mixin class for executing cypher

    Two execution modes:
    - __call__
    - estimate
    """

    def __init__(self, driver, namespace):
        super().__init__()
        self.namespace = namespace
        self.driver = driver
        self.estimate = False

    def _make_params(self, graph_name, config=None):
        if graph_name:
            return {
                "graph_name": graph_name,
                "config": config,
            }
        return {"config": config}

    def _make_call(self, arg1, arg2=None):
        """
        :param arg1: graphName (str) or config (dict)
        :param arg2: dict, mandatory is arg1 is not dict
        """
        if isinstance(arg1, dict):
            graph_name = None
            config = arg1
            cypher = f"CALL {self.procedure_name}($config)"
        else:
            graph_name = arg1
            config = arg2
            cypher = f"CALL {self.procedure_name}($graph_name, $config)"
        return self.run_cypher(
            cypher,
            self._make_params(graph_name, config)
        )

    def __call__(self, arg1, arg2=None):
        """
        """
        self.estimate = False
        return self._make_call(arg1, arg2)

    def estimate(self, arg1, arg2=None):
        """Run algorithm and write results back into Neo4j
        Returns some stats about algorithm execution
        """
        self.estimate = True
        self._make_call(arg1, arg2)

    @property
    def procedure_name(self):
        pn = self.namespace + "." + self.suffix
        if self.estimate:
            return pn + ".estimate"
        return pn


class AlgoWrite(AlgoMixin):
    suffix = "write"


class AlgoStream(AlgoMixin):
    suffix = "stream"


class AlgoMutate(AlgoMixin):
    suffix = "mutate"


class AlgoStats(AlgoMixin):
    suffix = "stats"

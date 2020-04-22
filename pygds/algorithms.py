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


class EstimateMixin:

    def estimate(self, graph_name, algo_config=None):
        """Run algorithm and write results back into Neo4j
        Returns some stats about algorithm execution
        """
        proc_name = self.procedure_name + ".estimate"
        cypher = f"CALL {proc_name}($graph_name, $algo_config)"
        return self.run_cypher(cypher, {
            "graph_name": graph_name,
            "algo_config": algo_config,
        })


class AlgoMixin(EstimateMixin, Neo4jRunner):

    return_data = True

    def __init__(self, driver, namespace):
        super().__init__()
        self.namespace = namespace
        self.driver = driver

    def _make_params(self, graph_name, algo_config=None):
        return {
            "graph_name": graph_name,
            "algo_config": algo_config,
        }

    def __call__(self, graph_name, algo_config=None):
        cypher = f"CALL {self.procedure_name}($graph_name, $algo_config)"
        return self.run_cypher(
            cypher,
            self._make_params(graph_name, algo_config), self.return_data
        )

    @property
    def procedure_name(self):
        return self.namespace + "." + self.suffix


class AlgoWrite(AlgoMixin):
    suffix = "write"


class AlgoStream(AlgoMixin):
    suffix = "stream"
    return_data = False


class AlgoStats(AlgoMixin):
    suffix = "stats"

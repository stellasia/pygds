
class Neo4jRunner:
    """Method to run Cypher queries
    """
    def run_cypher(self, cypher, params, get_data=True):
        with self.driver.session() as s:
            r = s.run(cypher, params)
        if get_data:
            data = r.data()
            return data
        return r


class Neo4jRunner:
    """Method to run Cypher queries
    """
    def run_cypher(self, cypher, params):
        with self.driver.session() as s:
            result = s.run(cypher, params)
            return result.data()


class Neo4jRunner:
    def run_cypher(self, cypher, params, get_data=True):
        with self.driver.session() as s:
            r = s.run(cypher, params)
        if get_data:
            data = r.data()
            return data
        return r

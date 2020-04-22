# pygds

A python wrapper to call [Neo4j Graph Data Science](https://neo4j.com/docs/graph-data-science/current/) procedure from python using the Neo4j python driver


### Overview

The goal of this package is to be able to use the same syntax as Cypher. For instance, if you write:

```
CALL gds.graph.create("graph", "*", "*")
```

The python equivalent would be:

```
gds.graph.create("graph", "*", "*")
```

Of course, more complex parameters are possible and this will also work:

```
gds.graph.create("graph", "User", 
	{
		"FOLLOWS": {
			"type": "FOLLOWS",
			"orientation": "NATURAL",
			"aggregation": "SUM"
		}
	}
)
```


Please refer to https://neo4j.com/docs/graph-data-science/current/ to get a list of available procedures from the GDS.


## Installation

This package is available on PyPI, so you can:

    pip install pygds


## Usage

The connection to the database is managed through the `GDS` object as follows:

```python
from pygds import GDS

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "<YOUR_PASSWORD>")


with GDS(URI, auth=AUTH) as gds:
	gds.graph.create("graph", "*", "*")
	# gds.
	# etc...
```

### Return values

There are three cases:


### Stream Procedures

The return value is a [BoltStatementResult](https://neo4j.com/docs/api/python-driver/1.7/results.html#neo4j.BoltStatementResult). It can be consumed with:

```python
result = gds.pageRank.stream("graph")
for record in result:
	print(record.get("nodeId"))
```


### Functions

The returned value is a single floatting point number.

Example:

```python
>>> gds.alpha.similarity.euclideanDistance([1, 2], [0, 1])
1.4142135623730951
```


### Write, stats and estimate

The return value is a dict containing all "yielded" fields from the procedure.


### Exceptions

All exceptions are defered to the GDS, no check is performed over the procedure you are trying to call. For instance, trying to call a non-existing procedure such as `gds.toto` will raise:

```
neobolt.exceptions.ClientError: There is no procedure with the name `gds.toto` registered for this database instance. Please ensure you've spelled the procedure name correctly and that the procedure is properly deployed.
```

### Projected graphs

You can use the following structure to make sure the projected graph will be deleted even if there are some errors with the algorithm:

```python
with GDS(URI, auth=AUTH) as gds:
	gds.graph.create("graph", "*", "*")
	try:
		gds.louvain.write("graph", {"writeProperty": "louvain"})
	except Exception as e:
		print(e)
	finally:
		gds.drop("graph")
```


## Known issues

1. This package has not really been tested for functions yet.


## Developer



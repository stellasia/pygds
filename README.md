# pygds

A python wrapper to call [Neo4j Graph Data Science](https://neo4j.com/docs/graph-data-science/current/) procedure from python using the Neo4j python driver

**WARNING** this package is under development and has not beeen fully tested yet. Please report issues if you find any bug. Thanks.


## Overview

The goal of this package is to be able to use the same syntax as Cypher. For instance, if you write:

```cypher
CALL gds.graph.create("graph", "*", "*")
```

The python equivalent would be:

```pythyon
gds.graph.create("graph", "*", "*")
```

Of course, more complex parameters are possible and this will also work:

```python
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


**WARNING** procedures that require a node as parameter will not work for now (shortest path and link prediction procedures for instance)


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


The return value is a list of dictionnaries whose keys are the expected return values from the procedure. It can be consumed with:

```python
result = gds.pageRank.stream("graph")
for record in result:
    print(record.get("nodeId"))
```


In case of functions, the result is a floating point number corresponding to the value of the function.


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
2. Shortest path procedures and link prediction functions does not work (like all other procedure expecting nodes as paramterrs)

## Developer



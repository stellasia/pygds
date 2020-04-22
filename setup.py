import setuptools


setuptools.setup(
    name="pygds",
    version="0.1.0",
    author="Estelle Scifo",
    description="A python wrapper around the Neo4j Graph Data Science Library",
    url="https://github.com/stellasia/pygds",
    packages=["pygds"],
    python_requires='>=3.6',
    install_requires=["neo4j"]
)

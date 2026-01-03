from typing import override
from domain.models.graph_job_result import GraphJobResult, get_graph_result
from domain.models.job import Job
from domain.settings import get_settings
from services.graph_operator.queries import queries
from neo4j import GraphDatabase
from domain.graph_operator.graph_operator_interface import GraphOperatorInterface

settings = get_settings()


class Neo4jGraphOperator(GraphOperatorInterface):

    def __init__(self):
        uri = settings.neo4j_uri
        user = settings.neo4j_user
        password = settings.neo4j_password
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

        self.operations = {"min_path": self.min_path, "all_paths": self.all_paths, "max_distance": self.max_distance,
                           "cluster_identification": self.cluster_identification, "high_connectivity_nodes": self.high_connectivity_nodes,
                           "nodes_by_connectivity": self.nodes_by_connectivity, "isolated_nodes": self.isolated_nodes
                           }

    @override
    def execute_job(self, job: Job) -> GraphJobResult:
        try:
            result = self.operations[job.operation](**job.get_valid_payload())
            errors = {}
        except Exception as e:
            result = {}
            errors = {"error": str(e)}
        return get_graph_result(job, result, errors)

    @override
    def min_path(self, origin_word: str, destination_word: str) -> dict:
        with self.driver.session() as session:
            record = session.run(queries['min_path'], start=origin_word, end=destination_word).single()

        return {"path": record["path"] if record else None}

    @override
    def all_paths(self, origin_word: str, destination_word: str, max_depth=5) -> dict:
        with self.driver.session() as session:
            result = session.run(queries['all_paths'], start=origin_word, end=destination_word, max_depth=max_depth, max_paths=50)

        return {"paths": [r["path"] for r in result]}

    @override
    def max_distance(self, origin_word: str) -> dict:
        with self.driver.session() as session:
            record = session.run(queries['max_distance'], start=origin_word).single()

        return {"max_distance": record["max_distance"] if record else 0}

    @override
    def cluster_identification(self) -> dict:
        with self.driver.session() as session:
            result = session.run(queries['cluster_identification'])

        return {"clusters": [{"word": r["word"], "component": r["componentId"]} for r in result]}

    @override
    def high_connectivity_nodes(self, max_nodes: int = 10) -> dict:
        with self.driver.session() as session:
            result = session.run(queries['high_connectivity_nodes'], limit=max_nodes)

        return {"nodes": [{"word": r["word"], "degree": r["degree"]} for r in result]}

    @override
    def nodes_by_connectivity(self) -> dict:
        with self.driver.session() as session:
            result = session.run(queries['nodes_by_connectivity'])

        return {"nodes": [{"word": r["word"], "degree": r["degree"]} for r in result]}

    @override
    def isolated_nodes(self) -> dict:
        with self.driver.session() as session:
            result = session.run(queries['isolated_nodes'])
            words = [r["word"] for r in result]

        return {"isolated_nodes": words}

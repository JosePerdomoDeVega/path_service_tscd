from services.graph_operator.neo4j_graph_operator import Neo4jGraphOperator
from domain.settings import get_settings
from domain.graph_operator.graph_operator_interface import GraphOperatorInterface
from services.logger.logger import get_logger

settings = get_settings()
logger = get_logger()


def get_graph_operator() -> GraphOperatorInterface:
    graph_operator = None
    if settings.graph_operator_implementation == "NEO4J":
        graph_operator = Neo4jGraphOperator()
        logger.info(f"Using {settings.graph_operator_implementation} as graph operator")
    return graph_operator

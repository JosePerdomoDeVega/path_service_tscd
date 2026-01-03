from abc import ABC, abstractmethod
from typing import Optional
from domain.cache.cache_manager_interface import CacheManagerInterface
from domain.models.graph_job_result import GraphJobResult
from domain.models.job import Job


class GraphOperatorInterface(ABC):
    """
    Abstract interface for graph operations.
    Each method represents a graph computation that is enqueued as a job.
    Results can be cached/retrieved via a cache manager.
    """

    cache_manager: CacheManagerInterface

    @abstractmethod
    def execute_job(self, job: Job) -> GraphJobResult:
        pass


    @abstractmethod
    def min_path(self, origin_word: str, destination_word: str) -> dict:
        """
        Enqueue a job to compute the shortest path between two words.

        :param origin_word: The starting word.
        :param destination_word: The ending word.
        :return: The job_id assigned to this operation.
        """
        pass

    @abstractmethod
    def all_paths(self, origin_word: str, destination_word: str, max_depth: Optional[int] = 10) -> dict:
        """
        Enqueue a job to compute all paths (up to max_depth) between two words.

        :param origin_word: The starting word.
        :param destination_word: The ending word.
        :param max_depth: Optional maximum number of paths to retrieve.
        :return: The job_id assigned to this operation.
        """
        pass

    @abstractmethod
    def max_distance(self, target_word: str) -> dict:
        """
        Enqueue a job to compute the maximum distance from a given word to any other node.

        :param target_word: The word from which distance is measured.
        :return: The job_id assigned to this operation.
        """
        pass

    @abstractmethod
    def cluster_identification(self) -> dict:
        """
        Enqueue a job to identify clusters (connected components) in the graph.

        :return: The job_id assigned to this operation.
        """
        pass

    @abstractmethod
    def high_connectivity_nodes(self, max_nodes: int = 10) -> dict:
        """
        Enqueue a job to retrieve the nodes with the highest connectivity.

        :param max_nodes: Maximum number of top nodes to retrieve.
        :return: The job_id assigned to this operation.
        """
        pass

    @abstractmethod
    def nodes_by_connectivity(self, n) -> dict:
        """
        Enqueue a job to retrieve all nodes sorted by connectivity degree.

        :return: A JSON like object containing nodes by connectivity degree.
        """
        pass

    @abstractmethod
    def isolated_nodes(self) -> dict:
        """
        Enqueue a job to retrieve all isolated nodes (nodes with no connections).

        :return: A JSON like object containing the isolated nodes.
        """
        pass

min_path_query = """
        MATCH (start:Word {value: $start}), (end:Word {value: $end})
        MATCH p = shortestPath((start)-[:CONNECTED*]-(end))
        RETURN [n IN nodes(p) | n.value] AS path
        """

all_paths_query = """
    CALL apoc.path.expandConfig(
  $start,
  {
    relationshipFilter: "CONNECTED",
    maxLevel: $max_depth,
    limit: $max_paths,
    endNodes: [$end]
  }
)
YIELD path
RETURN [n IN nodes(path) | n.value] AS path

    """

max_distance_query = """
        MATCH (start:Word {value: $start})
        MATCH p = (start)-[:CONNECTED*]-(n)
        WHERE n <> start
        RETURN max(length(p)) AS max_distance
        """

cluster_identification_query = """
        CALL gds.graph.project('wordGraph', 'Word', 'CONNECTED');
        CALL gds.wcc.stream('wordGraph')
        YIELD nodeId, componentId
        RETURN gds.util.asNode(nodeId).value AS word, componentId
        """

high_connectivity_query = """
        MATCH (n:Word)-[r:CONNECTED]-()
        RETURN n.value AS word, count(r) AS degree
        ORDER BY degree DESC
        LIMIT $limit
        """

nodes_by_connectivity_query = """
        MATCH (n:Word)-[r:CONNECTED]-()
        RETURN n.value AS word, count(r) AS degree
        ORDER BY degree DESC
        """

isolated_nodes_query = """
        MATCH (n:Word)
        WHERE NOT (n)-[:CONNECTED]-()
        RETURN n.value AS word
        """

queries = {
    "min_path": min_path_query,
    "all_paths": all_paths_query,
    "max_distance": max_distance_query,
    "cluster_identification": cluster_identification_query,
    "high_connectivity": high_connectivity_query,
    "nodes_by_connectivity": nodes_by_connectivity_query,
    "isolated_nodes": isolated_nodes_query, }

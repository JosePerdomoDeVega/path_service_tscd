### Path Service (PS)

Path Service (PS) is the computation module of the system, responsible for executing graph algorithms requested by users. It operates as a background worker that consumes jobs from a message queue populated by the Graph Service Query module.

This service performs all graph traversal and analysis operations, including shortest path computation, path enumeration, connectivity analysis, and cluster detection. By isolating these algorithms in a dedicated service, the system can scale processing capacity independently from the public API and better manage computational load.

PS retrieves graph data from the graph database and applies the requested algorithms under predefined constraints to prevent excessive resource consumption. Once a job is completed, the service sends the results back to GSQ for persistence and delivery to the end user.

The worker-based design of PS improves fault tolerance and allows multiple instances to run in parallel, enabling horizontal scalability and efficient processing of large or complex graph queries.

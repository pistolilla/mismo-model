# mismo-model
Neo4j model using a small subset of MISMO database

### Instructions

1. Create a new blank project (or sandbox) in Neo4j
2. Run the commands written in [constraints.txt](constraints.txt)
3. Run the commands written in [dump.txt](dump.txt)

    Alternatively you can generate a new set of commands randomly by running
    ```bash
    python generate.py > dump.txt
    ```

4. Create random relationships between Employers and Addresses
    ```Cypher
    WITH range(1,1) as rng
    MATCH (a:Address)
    WITH collect(a) AS addresses, rng
    MATCH (e:Employer)
    WITH e, apoc.coll.randomItems(addresses, apoc.coll.randomItem(rng)) AS addresses
    FOREACH (a in addresses | CREATE (e)-[:HAS_ADDRESS_IN]->(a))
    ```

5. Create random relationships between Borrowers and Employers
    ```Cypher
    WITH range(1,1) as rng
    MATCH (a:Address)
    WITH collect(a) AS addresses, rng
    MATCH (e:Employer)
    WITH e, apoc.coll.randomItems(addresses, apoc.coll.randomItem(rng)) AS addresses
    FOREACH (a in addresses | CREATE (e)-[:HAS_ADDRESS_IN]->(a))
    ```

### Useful Queries

To delete everything and start over
```Cypher
MATCH ()-[r]-() DETACH DELETE r;
MATCH (n) DELETE n;
```

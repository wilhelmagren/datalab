# DuckDB

DuckDB is a relational (table-oriented) database management system (DBMS) that supports
the Structured Query Language (SQL). SQLite is the world's most widely deployed DBMS,
DuckDB adopts the ideas of SQLite regarding simplicity and embedded operation.

DuckDB has **no external dependencies**, neither for compilation nor during run-time. For
releases, the entire source tree of DuckDB is compiled into two files, a header and an
implementation file. For building, all that is required to build DuckDB is a working C++11
compiler.

For DuckDB, there is no DBMS server software to install, update and maintain. DuckDB does
not run as a separate process, but completely embedded within a host process. For the
analytical use cases that DuckDB targets, this has the additional advantage of
**high-speed data transfer** to and from the database.

DuckDB provides **transactional guarantees** (ACID properties) through their custom, bulk
optimized **Multi-Version Concurrency Control (MVCC)**. Data can be stored in persistent,
**single-file databases**. DuckDB supports secondary indexes to speed up queries trying to
find a single table entry.

**DuckDB is deeply integrated into Python and R for efficient interactive data analysis.**

DuckDB is designed to support **analytical query workloads**, online analytical processing
(OLAP). To efficiently support this workload, it is critical to reduce the amount of CPU
cycles that are expended per individual value. The state of the art in data management to
achieve this are either **vectorized or just-in-time query execution engines**. DuckDB
uses a **columnar-vectorized query execution engine**. This greatly reduces overhead
present in traditional systems such as PostgreSQL, MySQL, or SQLite which process each row
sequentially. Vectorized query execution leads to far better performance in OLAP queries.


## DuckDB vs PostgreSQL

### Designed for Analytics vs Transactional Workloads

- DuckDB is optimized for analytical workloads—think OLAP-style queries, data science, and fast aggregations on local files.

- PostgreSQL is a traditional relational database system built for transactional workloads—think web applications, CRUD operations, and ACID compliance for multi-user environments.

### Embedded vs Client-Server Architecture

- DuckDB runs in-process (embedded directly in applications) without a separate database server, making it lightweight and easy to integrate.

- PostgreSQL follows a client-server model, requiring a running database instance, authentication mechanisms, and network connections.

### Columnar vs Row-Based Storage

- DuckDB stores data in a columnar format, which is highly efficient for analytical queries that scan large datasets.
- PostgreSQL uses a row-based format, better suited for transactional workloads where individual records are frequently updated.

### Scalability & Distributed Capabilities

- DuckDB is not designed for distributed computing or clustering—it excels in local, single-node processing.
- PostgreSQL supports replication, sharding, and extensions like CitusDB for horizontal scaling.


## Installation

Installation CLI:

```
curl https://install.duckdb.org | sh
```

Installation Python library:

```
python3 -m pip install duckdb
```


Install `ducklake` and `postgres` extensions with:

```python
import duckdb

with duckdb.connection() as conn:
    conn.install_extension("postgres")
    conn.install_extension("ducklake")

```


## Connection options

When using DuckDB through `duckdb.sql()` it operates on an **in-memory** database, i.e.,
no tables are persisted on disk. Invoking the `duckdb.connect()` method without arguments
returns a connection, which also uses an in-memory database:

```python
import duckdb

conn = duckdb.connect()
conn.sql("SELECT 42 AS x").show()
```

## Persistent storage

The `duckdb.connect(dbname)` creates a connection to a **persistent** database. Any data
written to that connection will be persisted, and can be reloaded by reconnecting to the
same file, both from Python and from other DuckDB clients.

```python
import duckdb

# create a connection to a file called 'file.db'
con = duckdb.connect("file.db")
# create a table and load data into it
con.sql("CREATE TABLE test (i INTEGER)")
con.sql("INSERT INTO test VALUES (42)")
# query the table
con.table("test").show()
# explicitly close the connection
con.close()
# Note: connections also closed implicitly when they go out of scope
```

```python
import duckdb

with duckdb.connect("file.db") as con:
    con.sql("CREATE TABLE test (i INTEGER)")
    con.sql("INSERT INTO test VALUES (42)")
    con.table("test").show()
    # the context manager closes the connection automatically
```

### Configuration

```python
import duckdb

con = duckdb.connect(config = {'threads': 1})
```


## Usage Python


```python
import duckdb

duckdb.sql("SELECT 42").show()

┌───────┐
│  42   │
│ int32 │
├───────┤
│    42 │
└───────┘
```


### Data ingress

```python
import duckdb

duckdb.read_csv("example.csv")                # read a CSV file into a Relation
duckdb.read_parquet("example.parquet")        # read a Parquet file into a Relation
duckdb.read_json("example.json")              # read a JSON file into a Relation

duckdb.sql("SELECT * FROM 'example.csv'")     # directly query a CSV file
duckdb.sql("SELECT * FROM 'example.parquet'") # directly query a Parquet file
duckdb.sql("SELECT * FROM 'example.json'")    # directly query a JSON file
```


### Pandas query

```python
import duckdb
import pandas as pd

pandas_df = pd.DataFrame({"a": [42]})
duckdb.sql("SELECT * FROM pandas_df")
```


### Polars query


```python
import duckdb
import polars as pl

polars_df = pl.DataFrame({"a": [42]})
duckdb.sql("SELECT * FROM polars_df")

┌───────┐
│   a   │
│ int64 │
├───────┤
│    42 │
└───────┘
```


### Result conversion

```python
import duckdb

duckdb.sql("SELECT 42").fetchall()   # Python objects
duckdb.sql("SELECT 42").df()         # Pandas DataFrame
duckdb.sql("SELECT 42").pl()         # Polars DataFrame
duckdb.sql("SELECT 42").arrow()      # Arrow Table
duckdb.sql("SELECT 42").fetchnumpy() # NumPy Arrays
```


### Writing data to disk

```python
import duckdb

duckdb.sql("SELECT 42").write_parquet("out.parquet") # Write to a Parquet file
duckdb.sql("SELECT 42").write_csv("out.csv")         # Write to a CSV file
duckdb.sql("COPY (SELECT 42) TO 'out.parquet'")      # Copy to a Parquet file
```


## Loading and Installing Extensions

```python
import duckdb

con = duckdb.connect()
con.install_extension("spatial")
con.load_extension("spatial")
```


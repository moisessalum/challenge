# Challenge

## Files
* Dockerfile: Used to build the docker for the challenge.
* etl.py: Python process that extracts, transforms and loads the data from transactional sources to an OLAP / DWH destination.
* mongo_transactional.py: Python process that creates the MongoDB database on the Dockerfile.
* psql_analytical.sql: SQL process that creates the PSQL OLAP database on the Dockerfile.
* psql_transactional.sql: SQL process that creates the PSQL OLTP database on the Dockerfile.
* requirements.txt: Libraries needed to run the process on Python.
* .env_vars: Environment variables used on the process.

## How to run the process
1. Download all the files to the same folder.
1. Build the Dockerfile.
> docker build -t challenge .
1. Run the built docker in -it mode.
> docker run -it challenge
1. Start the PSQL and MongoDB services.
> /etc/init.d/postgresql start
> /etc/init.d/mongodb start
1. Source the environment variable file.
> source /.env_vars
 1. If you'd like to explore the dbs before and after the ETL pipeline is executed, the credentials will be listed below. Note: Remember to login as postgres user before accessing the Postgres database:
 > root:/# su postgres
 > postgres:/# psql -d olap
 > olap=#
 Or
 > postgres:/# psql -d oltp
 > oltp=#
 You can access the MongoDB database from root.
 > root:/# mongo
 > show dbs
 > transactional 0.000GB
1. Execute the etl.py script.
> python3 etl.py
1. The script will print 3 messages on the terminal.
> Customers done.
> Items done.
> Orders done.


## Logic behind the process
1. The Dockerfile builds a docker with 2 PSQL databases (one transactional database and another database that will be used as the DWH/OLAP) and 1 MongoDB database.
1. Both PSQL and MongoDB transactional databases are created with 3 tables/collections each: customers, items and orders.
1. The etl.py file extracts the data from both transactional sources, transforms the data and loads 3 tables into the DWH (PSQL "OLAP" database).


## Credentials
* OLTP database
 * user: postgres
 * password: P4ssw0rd!
 * host: localhost
 * database: oltp
 * port: 5432
 
* OLAP database
 * user: postgres
 * password: P4ssw0rd!
 * host: localhost
 * database: olap
 * port: 5432
 
* MongoDB database
 * host: localhost
 * port: 27017

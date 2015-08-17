#OPFlood
**_The script contains a minimum set of customers for PostgreSQL and Oracle. Designed for use SQL injection._**
```
Usage: opflood.py [-h] [-a ADDRESS] 
                  [-p PORT] [-u USER] [-w PASSWORD] [--install]
                  [-i DIALECT] [-d DATABASE] [-s SCHEMA] [-v VERBOSE] [-q QUIET] [--version]

Example:
Oracle: opflood.py -i oracle -a 10.0.0.1 -u system -w 123456 -d dbt -s 1.sql -s /schem/2.sql
PostgreSQL: opflood.py -i postgresql -a 10.0.0.2 -u system -w 123456 -d dbt -s 1.sql -s /shem/2.sql

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -a Server address, --address=Server address
                        Server address, default 'localhost'
  -p PORT, --port=PORT  Server port
  -u USER, --user=USER  username
  -w PASSWORD, --password=PASSWORD
                        Password
  -i {oracle or postgresql}, --dialect={oracle or postgresql}
                        Dialect of SQL {oracle, postgresql}
  -d DB name, --db=DB name
                        Name the connected database
  -s SCHEMA, --schema=SCHEMA
                        Database schema name(s)
  -v, --verbose         
  -q, --quiet           
  --install={oracle or postgresql or all}
                        Installing components
```


---
tags:
  - type/zettel
aliases:
created: 2025-11-06 10:32:53
---
# Auto Increment Behavior

## How each Database handle auto incrementing

Usually `INT`/`INTEGER` for (sqlite/mysql) and `SERIAL` for Postgres are sufficient for ID fields or auto incrementing but each DBMS is different

**MySQL:** For this, you have to provide AUTO_INCREMENT for DBMS to fill-in the field with proper ID

**Sqlite:** This DBMS is different, using `INT` is enough, when the value is null, it will attempt to auto increment it by default

**Postgres:** It has special type of it and it is called `SERIAL`
## References


## Questions/Thoughts
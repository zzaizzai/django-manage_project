



```
pg_dump -U postgres -h localhost -d manage_project > create_db.sql
pg_restore -U postgres -h localhost -d manage_project < create_db.sql
```
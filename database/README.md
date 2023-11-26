



```
pg_dump -Fc -U postgres -h localhost -d manage_project > backup.dump

pg_dump -U postgres -h localhost -d manage_project -E UTF8 > backup.sql
pg_restore -U postgres -h localhost -d manage_project > backup.dump
```
# DBUTILS
Some functions useful when working with a database, implemented in python.

## Set the environment variables
  - DB_HOST='localhost'  e.g. ``export DB_HOST='localhost'``
  - DB_USERNAME='username'
  - DB_PASSWORD='password'

## Example
```python
    d = DbManager(host=os.environ['DB_HOST'],
                  user=os.environ['DB_USERNAME'],
                  password=os.environ['DB_PASSWORD'])
    d.create_db(DB_DATABASENAME)
    d.use_db(DB_DATABASENAME)
    d.create_table(DB_TABLENAME, (<column_description>))
    d.insert_table_data(DB_TABLENAME, [<column_values>])
    d.delete_db(DB_DATABASENAME)
    d.close()
```

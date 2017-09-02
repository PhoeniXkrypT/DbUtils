# DBUTILS
Some functions useful when working with a database, implemented in python.

## Set the environment variables
  - DB_HOST='localhost'  e.g. ``export DB_HOST='localhost'``
  - DB_USERNAME='username'
  - DB_PASSWORD='password'

## Example usage
```python
    d = DbManager(host=os.environ['DB_HOST'],
                  user=os.environ['DB_USERNAME'],
                  password=os.environ['DB_PASSWORD'])
    d.create_db(<database_name>)
    d.use_db(<database_name>)
    d.create_table(<table_name>, (<column_description>))
    d.insert_table_data(<table_name>, [<column_values>])
    d.delete_db(<database_name>)
    d.close()
```

# Some notes and leason I learned during this Project

* SQL code that Django will execute in the database to create the table for your model.

**Syntax**
```
python manage.py sqlmigrate <app_name> <migrations_file_name>
```

**Example**
```
python manage.py sqlmigrate blog 0001
```

* You can create a custom database name for your model in the **Meta** class of the model using the **db_table** attribute.

**Solution**

```
class(.....):
    field.....
    field.....


    class Meta: 
        db_table = <custom_table_name>

```

* Queries with field lookup methods are built using two underscores, for example, **publish__ year**, but the same notation is also used for accessing fields of related *models*, such as **author__username**.

**Example**

```
Post.objects.filter(publish__year=2024, author__username="admin")
```
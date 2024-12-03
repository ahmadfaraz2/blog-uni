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

<!-- ## related_name 
**related_name** is used to make reverse relationships more discriptive

* For exmaple we have two models **Post** and **Comment**

**Example**

```
class Comment(models.Model):
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE, 
                            related_name="comments")
    name = models.CharField(max_length=80)


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date=("publish"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    body = models.TextField()
```

Here **Post** and **Comment** have one-to-many relationship:
* A single post can have multiple comments

So how will we access these comments, so for this we have to make a query

**Steps**

1. Retrive a single post: 
``` post = post.objects.get(id=1) ```
2. Now we have single post, now we will retrive all comments associated wit this single post by making a query.
```post.comments.all()```

Remember this **comments** we declare in the **Comment** Model of **post** field. -->


## related_name 

**related_name** is used to make reverse relationships more descriptive in Django models.

### Example:

Consider the following two models: **Post** and **Comment**.

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)

class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    body = models.TextField()
```

Here, **Post** and **Comment** have a one-to-many relationship:
- A single post can have multiple comments.

### Accessing Comments for a Post

To access the comments of a specific post, you can use the `related_name` attribute.

**Steps:**

1. Retrieve a single post:
    ```python
    post = Post.objects.get(id=1)
    ```

2. Retrieve all comments associated with this post:
    ```python
    post.comments.all()
    ```

The `comments` attribute, specified in the `Comment` model with `related_name`, allows you to access all comments related to the `post`.


This is the same thing we also doing with **django-taggit**.


## Custom Template Tags
* **simple_tag** vs **inclusion_tag**
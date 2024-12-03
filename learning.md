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


## Custom Template Tags and Filters

Django allows you to create your own template tags to perform custom actions.

### Custom Template Tags

1. **simple_tag** Processes the given data and returns a string

2. **inclusion_tag**: Processest the given data and and returns a __rendered template__

### Rules and Method to make **Custome Tags**
These tags must live insdie **django application**.

1. Create a new directory inside your django appliction
```
mkdir templatetags
```
2. Add an empty \_\_init\_\_.py file to it.
``` 
new-item templatetags/__init__.py 
```
3. Create another file in it and name it **custome_tags.py** or **<app_name\>_tags.py** file
```
new-item templatetags\<app_name>_tags.py 
```

## Simple template tag

### Syntax to create simple template tag
```python
from django import template 

register = template.Library()

@register.simple_tag
def total_posts(): 
    return Post.published.count() # any query that returns some "value"
``` 

#### Note
> Before using custom template tags, we have to make them  available for the template using the ```{% load %}```tag

### Syntax in template
```
{% load <custom_tag_file_name> %}

e.g
    {% load custom_tags %}
    {% load blog_tags %}

I have written {% tota_posts %} so far
```

### Important (highlight it)
**Template Tags** allow you to **process any data** and _add_ it to **any template** regardless of the **view executed**.

## Inclusion template tag

Using an **inclusion template tag**, you can **render a template** with **context variables**(dictionary) returned by your **template tag**.

### Syntax to create inclusion template tag
```python
@register.inclusion_tag("<template_that_will_be_rendered>") # "blog/post/latest_posts.html"
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}
```
Edit the "blog/post/latest_post.html"
```html
<ul>
    {% for post in latest_posts %}
    <li>
        <a href="{{post.get_absolute_url}}">{{post.title}}</a>
    </li>
    {% endfor %}
</ul>
```
Now you have to call the **tag** in any other template and pass parameter
```html
<h3>Latest Posts</h3>
{% show_latest_posts 3 %}
```

## Creating a template tag that returns Query Set

### Syantx
```python
from django.db.models import Count

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count("comments")).order_by("-total_comments")[:count]
```

### Usage in template
```html
<h3>Most Commented Posts</h3>

{% get_most_commented_posts as most_commented_posts %}
<ul>
    {% for post in most_commented_posts %}
        <li>
            <a href="{{post.get_absolute_url}}">{{post.title}}</a>
        </li>
    {% endfor %}
</ul>
```

## Implementing template filters

Open file in which you have made **custom tags**
```python
from django.utils.safestring import mark_safe
import markdown

@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
```

### Usage
```
{% load <custom_tag_file> %}

{{post.body|markdonw}}
```
This filter will transform the Markdown content into HTML.


### Summary

1. **Create the `templatetags` directory and the necessary files.**
2. **Define custom template tags and filters in `templatetags/custom_tags.py`.**
3. **Load and use the custom tags and filters in your templates with `{% load custom_tags %}`.**

This guide provides a straightforward way to create and use custom template tags and filters in Django, making it easier for anyone to follow and understand.
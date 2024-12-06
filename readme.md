# ThoughtCanvas Blog Application

ThoughtCanvas is a Django-based blog application that allows users to create, edit, and delete blog posts. It also includes user authentication features such as sign-up, login, and logout.

## Features

- User authentication (sign-up, login, logout)
- Create, edit, delete blog posts
- Display list of published posts
- View individual post details
- Add and manage tags for posts
- Custom template tags and filters
- Pagination for posts
- Comment on posts
- Share posts via email

## Requirements

- Python 3.x
- Django 4.x or higher
- django-taggit for tag management

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ahmadfaraz2/blog-uni.git
cd blog-uni
```

2. Create a virtual environment and activate it:

```bash
python -m virtualenv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Open your browser and go to `http://127.0.0.1:8000` to see the application.

## Configuration

### Time Zone

To adjust for a time zone difference of 5 hours ahead of your server time, set the `TIME_ZONE` in `settings.py`:

```python
USE_TZ = True
TIME_ZONE = 'Asia/Karachi'  # This is UTC+5
```

### Redirects

Set the login and logout redirect URLs in `settings.py`:

```python
LOGIN_REDIRECT_URL = 'blog:post_list'
```

## Usage

### User Authentication

- Sign up at `/accounts/signup/`
- Log in at `/accounts/login/`
- Log out at `/accounts/logout/`

### Post Management

- Create a new post at `/post/new/`
- Edit a post at `/post/<id>/edit/`
- Delete a post at `/post/<id>/delete/`

### Custom Template Tags

#### Total Posts

A custom template tag to count total posts for the logged-in user:

```python
@register.simple_tag
def total_posts(user):
    return Post.published.filter(author=user).count()
```

Usage in template:

```html
{% load custom_tags %}
<p>Total posts: {% total_posts request.user %}</p>
```

#### Most Commented Posts

A custom template tag to display most commented posts:

```python
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
```

Usage in template:

```html
{% get_most_commented_posts as most_commented_posts %}
<ul>
    {% for post in most_commented_posts %}
        <li><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>
```

## Branching Strategy

To add new features, create a new branch from the main branch:

```bash
git checkout -b feature/<feature_name>
```

After implementing the feature, push the branch to GitHub:

```bash
git push origin feature/<feature_name>
```

If you need to merge the feature branch with the main branch:

```bash
git checkout main
git merge feature/<feature_name>
```

## Contributing

If you would like to contribute to ThoughtCanvas, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Documentation
- Bootstrap Documentation
- django-taggit Documentation

---

By following the steps and configurations provided, you should be able to set up and run the ThoughtCanvas blog application. If you have any questions or need further assistance, feel free to reach out.
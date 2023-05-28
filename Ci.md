Testing is a essential part of sSoftware Development Life Cycle(SDLC). A software or a application should be tested thoroughly before publishing it to the public. 

Over time, testing become time consuming, as you develop new feature and improve your application gradually, you have to run your application test cases with hand. but what if you just write code, push it to the somewhere like github and someone would test your application against your test-cases and notify you if any test failed. 

That's where Github action comes to the picture, with github action you can run your application test to make sure your new feature isn't breaking existing code and introducing a new bug. With Github action, we can construct a CI/CD pipeline for our application, 

<!-- 
Now you might be wondering what is CI/CD actually is? 
Well, CI stands for Continuous Integration and CD stands for Continuous Deployment. Let's learn this from example, imagine you're building a LEGO tower. CI/CD is like having a magical robot that makes building and testing your tower really easy and quick. 

CI means whenever you add a new piece to your LEGO tower, the magical robot immediately checks if everything still fits together nicely. It makes sure that the tower doesn't fall down when you add a new piece, so you can fix any problems right away.

On the other hand, CD means that once your LEGO tower is all built and tested, the magical robot automatically puts it on display for everyone to see. It takes care of all the steps needed to show your tower to the world, like putting it on a nice platform and turning on the lights.

So, CI/CD is like having a magical robot that helps you build and test your LEGO tower at every step, and when it's all ready, it shows your tower to everyone without you having to do all the work manually.
 -->


In this blog, we will be focusing CI part with the help of github action. We will create a simple django application, write some test-cases and I will demonstrate how you can leverage the power of Github action.


## Table of Content

1. [Creating a Django application](#create)
   
2. [Setting up our Django application](#set)
   
3. [Writing test for our application](#test)

4. [Setting up a Github repository](#repo)

5. [Configuring Github action](#action)
   
6. [Implementing CI](#implement)

7. [Conclusion](#conclusion)

8.  [Configuring `passenger_wsgi.py`](#passenger)
   
9.  [Managing database](#database)

10. [Creating a new separate subdomain to serve media files](#media)




<h2 id="create">Creating a Django application</h2>


First, create a virtual environment and activate it:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Next, install Django, and DRF and create a new Django project:

```
$ pip install django djangorestframework
$ django-admin startproject library .
```


Similarly, let's crate a new app called `books`
```
python manage.py startapp books
```

Now, add `rest_framework` and `books` to the installed apps list in the settings:
```
# library/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'books',
]
```


<h2 id="create">Setting up our Django application</h2>

We have created a basic django project called `library` and a new app `books`

Now, let's build our book app model 
```
# book/models.py

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

```

After that, create a migration and migrate
```
$ python manage.py makemigrations
$ python manage.py migrate
```

Now, let's create a serializer class for `Book` model, Create a new file called `serializers.py` on `books` app directory

```
# book/serializers.py

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_date', 'description', 'price', 'created_at', 'updated_at']
```


Similarly, create a view to perform different operation in `book` model

```
# book/views.py

from rest_framework import viewsets
from .serializers import BookSerializer
from .models import Book

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

Finally, let's configure `url_patterns` for book, so that we can access it from browser

```
# book/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
```

Now, if you enter `http://127.0.0.1:8000/books/` on your browser you can access browse-able api 


<h2 id="test">Writing test for our application </h2>


We have created a basic app. Now, let's write some test-cases for our application. We wil be using pytest to test our application.


First, install `pytest` and `pytest-django`
```
pip install pytest pytest-django
```

Create pytest configuration file on root of the project `pytest.ini` 
```
[pytest]
DJANGO_SETTINGS_MODULE=library.settings
```

Create a new `tests` folder in `books` model

Create a module prefixing with test `test_books.py` in `test` folder

Make sure to prefix with `test`. So that pytest can detect our test-cases

Now, open up a `test_books.py` file and let's write a test for POST method for `/books/` endpoints
```
# books/tests/test_books.py

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_data_is_invalid_returns_400(self):
        client = APIClient()
        response = client.post("/books/", {"author": "Henry", "price": 300})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self):
        client = APIClient()
        response = client.post(
            "/books/",
            {
                "title": "Atomic Habits",
                "author": "James Clear",
                "publication_date": "2020-12-8",
                "description": "about habit",
                "price": 4000,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
```

For the sake of simplicity, we will write only two test-cases. But if you are curious, feel free to increase it.


Alright, we wrote the test, now let's run it to check whether our test passes or not.
```
$ pytest
```

```
collected 2 items                                                 

books/tests/test_books.py ..                                [100%]

======================== 2 passed in 0.50s ========================
```

Alright, we have the passing test.



<h2 id="repo">Setting up a Github repository</h2>

First, create a github repository in github 



Then, create a new git repo locally and push it to the github

Note: make sure to replace `git@github.com:chapainaashish/library-ci.git` with your github repo url
```
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:chapainaashish/library-ci.git
git push -u origin main
```


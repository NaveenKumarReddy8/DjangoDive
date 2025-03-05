# Django


## Django Architecture


This is how Django handles HTTP requests and generates responses:
1) A web browser requests a page by its URL and the web server passes the HTTP request to Django.
2) Django runs through its configured URL patterns and stops at the first one that matches the requested URL.
3) Django executes the view that corresponds to the matched URL pattern.
4) The view potentially uses data models to retrieve information from the database.
5) Data models provide data definitions and behaviors. They are used to query the database.
6) The view renders a template (usually HTML) to display the data and returns it with an HTTP response.

### Django Project Layout

* manage.py: This is a command-line utility used to interact with your project. You won’t usually need to edit this file.
* djangodive/: This is the Python package for your project, which consists of the following files:
* 
    * __init__.py: An empty file that tells Python to treat the mysite directory as a Python module.
    * asgi.py: This is the configuration to run your project as an ASGI application with ASGI-compatible web servers. ASGI is the emerging Python standard for asynchronous web servers and applications.
    * settings.py: This indicates settings and configuration for your project and contains initial default settings.
    * urls.py: This is the place where your URL patterns live. Each URL defined here is mapped to a view.
    * wsgi.py: This is the configuration to run your project as a Web Server Gateway Interface (WSGI) application with WSGI-compatible web servers.

### When QuerySets are evaluated

Creating a QuerySet doesn’t involve any database activity until it is evaluated. QuerySets will usually
return another unevaluated QuerySet. You can concatenate as many filters as you like to a QuerySet,
and you will not hit the database until the QuerySet is evaluated. When a QuerySet is evaluated, it
translates into a SQL query to the database.

QuerySets are only evaluated in the following cases:

* The first time you iterate over them
* When you slice them, for instance, Post.objects.all()[:3]
* When you pickle or cache them
* When you call repr() or len() on them
* When you explicitly call list() on them
* When you test them in a statement, such as bool(), or, and, or if
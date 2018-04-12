import django.dispatch


book_published = django.dispatch.Signal(providing_args=["book", "author"])
Voice
=====

A votebox for letting users request features.

Setup
-----

    pip install voice

In `settings.py`:

    INSTALLED_APPS = (
        ...
        'voice',
    )

In `urls.py`:

    urlpatterns = patterns('',
        (r'^$', include('voice.urls', namespace='voice')),
    )

For further usage, look at the provided `example_project`.

Screens
-------

![admin view](http://s3.amazonaws.com/jarodlrandom/admin_view.png)

![feature view](http://s3.amazonaws.com/jarodlrandom/feature_view.png)

![main view](http://s3.amazonaws.com/jarodlrandom/main_view.png)

![vote view](http://s3.amazonaws.com/jarodlrandom/vote_view.png)

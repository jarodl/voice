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

For further usage, look at the provided example_project.

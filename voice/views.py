from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, \
        Http404, HttpResponseNotModified
from django.contrib import messages

from voice import settings
from voice.models import Feature
from voice.forms import VoteForm, FeatureForm 

def index(request):
    feature_id = None
    form = VoteForm()

    grouped = []
    group = []
    features = Feature.objects.all()
    for i, feature in enumerate(features):
        group.append(feature)
        if (i + 1) % 4 == 0:
            grouped.append(group)
            group = []
    if len(group) > 0:
        grouped.append(group)

    context = RequestContext(request, {
        'grouped_features': grouped,
        'form': form,
        'feature_id': feature_id,
        'request': request,
        })

    return render_to_response('voice/index.html', context)

def feature(request, feature_id):
    feature = Feature.objects.get(id=feature_id)

    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.feature = feature
            vote.save()
            messages.success(request, 'Vote successfully submitted!')
    else:
        form = VoteForm()

    context = RequestContext(request, {
        'form': form,
        'request': request,
        'feature': feature,
        })

    return render_to_response('voice/feature.html', context)

def new_feature(request):
    if request.method == 'POST':
        form = FeatureForm(request.POST)
    else:
        form = FeatureForm()

    context = RequestContext(request, {
        'form': form,
        })
    return render_to_response('voice/new_feature.html', context)

def admin(request):
    features = Feature.objects.all()
    return render_to_response('voice/admin.html', {
        'request': request,
        'features': features,
        })

def static_media(request, path):
    """
    Taken from django-sentry:
    http://github.com/dcramer/django-sentry

    Serve static files below a given point in the directory structure.
    """
    from django.utils.http import http_date
    from django.views.static import was_modified_since
    import mimetypes
    import os.path
    import posixpath
    import stat
    import urllib

    document_root = os.path.join(settings.ROOT, 'static')
    print document_root

    path = posixpath.normpath(urllib.unquote(path))
    path = path.lstrip('/')
    newpath = ''
    for part in path.split('/'):
        if not part:
            # Strip empty path components.
            continue
        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            # Strip '.' and '..' in path.
            continue
        newpath = os.path.join(newpath, part).replace('\\', '/')
    if newpath and path != newpath:
        return HttpResponseRedirect(newpath)
    fullpath = os.path.join(document_root, newpath)
    if os.path.isdir(fullpath):
        raise Http404("Directory indexes are not allowed here.")
    if not os.path.exists(fullpath):
        raise Http404('"%s" does not exist' % fullpath)
    # Respect the If-Modified-Since header.
    statobj = os.stat(fullpath)
    mimetype = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj[stat.ST_MTIME], statobj[stat.ST_SIZE]):
        return HttpResponseNotModified(mimetype=mimetype)
    contents = open(fullpath, 'rb').read()
    response = HttpResponse(contents, mimetype=mimetype)
    response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    response["Content-Length"] = len(contents)
    return response

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, \
        Http404, HttpResponseNotModified
from django.contrib import messages

from voice import settings
from voice.models import Request
from voice.forms import VoteForm

def index(request):
    request_id = None
    if request.method == 'POST':
        form = VoteForm(request.POST)
        request_id = request.POST.get('request')
        if form.is_valid():
            vote = form.save(commit=False)
            vote.request = Request.objects.get(id=request_id)
            vote.save()
            messages.success(request, 'Vote successfully submitted!')
    else:
        form = VoteForm()

    grouped_requests = []
    group = []
    all_requests = Request.objects.all()
    for i, user_request in enumerate(all_requests):
        group.append(user_request)
        if (i + 1) % 4 == 0:
            grouped_requests.append(group)
            group = []
    if len(group) > 0:
        grouped_requests.append(group)

    context = RequestContext(request, {
        'user_requests': grouped_requests,
        'vote_form': form,
        'request_id': request_id,
        'request': request,
        })

    return render_to_response('voice/index.html', context)

def admin(request):
    user_requests = Request.objects.all()
    return render_to_response('voice/admin.html', {
        'request': request,
        'user_requests': user_requests,
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

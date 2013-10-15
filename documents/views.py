from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.template import RequestContext
from models import Document
from django.conf import settings
import django.views.static

def upload_file(request):
    if not request.user.is_authenticated():
        return HttpResponse('fail unlogin')
    try:
        upload_file = request.FILES['file']
        doc = Document(owner = request.user, public = True, doc_name = upload_file.name, doc_file = upload_file)
        doc.save()
    except:
        return HttpResponse('fail upload fail')
    else:
        return HttpResponseRedirect('/homepage/')

def render_pdf(request, _id):
    return render_to_response(
        'render.html',
        {
            'doc_id' : _id,
        },
    )

def serve_pdf(request, doc_id):
    doc = Document.objects.get(id = doc_id)
    if doc is None:
        return HttpResponseNotFound()
    path = doc.doc_file.path
    print path
    return django.views.static.serve(request, path, '')

def getDoc(user):
    return Document.objects.all().filter(owner=user)
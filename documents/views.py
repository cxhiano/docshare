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
        doc = Document(owner = request.user, public = False, doc_name = upload_file.name, doc_file = upload_file)
        doc.save()
    except:
        return HttpResponse('fail upload fail')
    else:
        return HttpResponseRedirect('/homepage/')

def render_pdf(request, _id):
    doc = Document.objects.get(id = _id)
    return render_to_response(
        'render.html',
        {
            'doc_id' : _id,
	    'login_user': request.user,
            'current_user': doc.owner,
        },

        context_instance = RequestContext(request)
    )

def serve_pdf(request, doc_id):
    doc = Document.objects.get(id = doc_id)
    if doc is None:
        return HttpResponseNotFound()
    path = doc.doc_file.path
    if doc.public or doc.owner == request.user:
        return django.views.static.serve(request, path[len(settings.MEDIA_ROOT):].replace('\\', '/'), settings.MEDIA_ROOT)
    else:
        pass

def getDoc(user):
    return Document.objects.all().filter(owner=user)

def delete_doc(request, _id):
    doc = Document.objects.get(id = _id)
    if doc and doc.owner == request.user:
        doc.delete()
    return HttpResponseRedirect('/homepage/')

def switch_public_status(request, _id):
    doc = Document.objects.get(id = _id)
    if doc and doc.owner == request.user:
        doc.public = not doc.public
        doc.save()
    return HttpResponseRedirect('/homepage/')

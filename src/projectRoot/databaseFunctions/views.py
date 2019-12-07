from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .forms import documentForm
from .models import document

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        context['url'] = fs.url(name)
    return render(request, 'upload.html',context)

def document_list(request):
    documents = document.objects.all()
    return render(request, 'documents.html', {
        'Documents' : documents
    })

def upload_document(request):
    if request.method == 'POST':
        form = documentForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form Saved")
            form.save()
            return HttpResponseRedirect('/documents')
    else:
        form = documentForm()
    return render(request, 'upload_document.html', {
        'form': form
    })

def delete_document(request, pk):
    if request.method =='POST':
        d = document.objects.get(pk=pk)
        d.delete()
        return HttpResponseRedirect('/documents')


# ccbv.co.uk
class DocumentList(ListView):
    model = document
    template_name = 'class_documents.html'
    context_object_name = "Documents"

class DocumentUpload(CreateView):
    model = document
    fields = ('name', 'document')
    success_url = reverse_lazy('DocumentList')
    template_name = 'upload_document.html'
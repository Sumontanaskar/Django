from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect
from .models import Dreamreal
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .forms import handle_uploaded_file, handle_file
from django.utils.dateparse import parse_datetime
import os

# Create your views here.
def index(request):
    all_host = Dreamreal.objects.all()
    distinct_host = Dreamreal.objects.order_by('host').values('host').distinct()
    host = []
    for list in distinct_host:
        host.append(list['host'])
    return render(request, 'myapp/index.html', {'all_host': all_host, 'distinct_host': host})

#Details id replied
def detail(request, host_id):
    try:
        host = Dreamreal.objects.get(pk=host_id)
    except Dreamreal.DoesNotExist:
        raise Http404("Host not exist")
    return render(request, 'myapp/details.html', {'host': host})

def search(request):
    h = request.GET.get("h")
    d = request.GET.get("d")
    no_data = ''
    try:
        if not h and not d:
            error = 'Please enter valid Details'
            return render(request, 'myapp/results.html', {'error':error})
        if h and d:
            search = Dreamreal.objects.filter(
                Q(host=h),
                Q(date=d)
                  ).distinct()
        if not d:
            search = Dreamreal.objects.filter(
                Q(host=h),
                  ).distinct().order_by('-date')
        if not h:
            search = Dreamreal.objects.filter(
                Q(date=d),
            ).distinct().order_by('host')
        if not len(search):
            no_data = 'No Data in Database'
        return render(request, 'myapp/results.html', {'all_host': search, 'no_data': no_data})
    except Exception as error:
        return render(request, 'myapp/results.html', {'error': error})


#Upload file
def upload(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            handle_uploaded_file(request.FILES['myfile'])
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            bunch_date = Dreamreal.objects.values_list('date').distinct().order_by('-date')
            return render(request, 'myapp/upload.html', {
                'uploaded_file_url': uploaded_file_url,
                'bunch_date': bunch_date
            })
        bunch_date = Dreamreal.objects.values_list('date').distinct().order_by('-date')
        return render(request, 'myapp/upload.html', {'bunch_date': bunch_date})
    except Exception as e:
        e = 'Please upload a valid file'
        return render(request, 'myapp/upload.html', {'error': e})

#Details for hostname in index page response

def host_details(request):
    hostname = request.GET.get('hostname')
    all_host = Dreamreal.objects.filter(host=hostname).order_by('-date')
    return render(request, 'myapp/results.html', {'all_host': all_host, 'hostname': hostname})
#Auto upload
def AutoUpload(request):
    path = 'media/'
    csv_list = os.listdir(path)
    for file in csv_list:
        path = 'media/'+file
        f = open( path, 'r')

        handle_file(f)
    all_host = Dreamreal.objects.all()
    distinct_host = Dreamreal.objects.order_by('host').values('host').distinct()
    host = []
    for list in distinct_host:
        host.append(list['host'])
    return render(request, 'myapp/index.html', {'all_host': all_host, 'distinct_host': host})

from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect
from .models import Dreamreal
from django.core.files.storage import FileSystemStorage
from .forms import handle_uploaded_file
import datetime

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

def results(request):
    if request.method == "POST":
        hostname = request.POST['hostname']
        date = request.POST['date']
        try:
	        datetime.datetime.strptime(date, '%Y-%m-%d')
        	pass
        except ValueError:
            raise Http404("Error: Insert Valid Date as format yyyy-mm-dd ")
        format = type(date)
        try:
                all_host = Dreamreal.objects.filter(host=hostname, date=date).order_by('-date')
                print (hostname, date)
                return render(request, 'myapp/results.html', {'all_host': all_host, 'hostname': hostname, 'date': date})
        except:
                all_host = Dreamreal.objects.filter(host=hostname).order_by('-date')
                print (hostname, date)
                return render(request, 'myapp/results.html', {'all_host': all_host, 'hostname': hostname, 'date': date})
        finally:
                all_host = Dreamreal.objects.filter(date=date).order_by('-date')
                print (hostname, date)
                return render(request, 'myapp/results.html', {'all_host': all_host, 'hostname': hostname, 'date': date})      
#        print (hostname, date)
 #       return render(request, 'myapp/results.html', {'all_host': all_host, 'hostname': hostname, 'date': date})

#Upload file
def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        handle_uploaded_file(request.FILES['myfile'])
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'myapp/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    all_host = Dreamreal.objects.all()
    return render(request, 'myapp/upload.html', {'all_host': all_host})

#Details for hostname in index page response

def host_details(request):
    hostname = request.GET.get('hostname')
    all_host = Dreamreal.objects.filter(host=hostname).order_by('-date')
    return render(request, 'myapp/results.html', {'all_host': all_host, 'hostname': hostname})

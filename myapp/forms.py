from .models import Dreamreal
import datetime


def Dateformat(date):
    try :
        return datetime.datetime.strptime(date, '%m-%d-%Y').strftime('%Y-%m-%d')
    except:
        return datetime.datetime.strptime(date, '%m-%d-%y').strftime('%Y-%m-%d')

def handle_uploaded_file(f):
    i = 0
    for chunk in f:
        chunk = chunk.decode("utf-8")
        chunk = chunk.split(',')
        data = Dreamreal()
        if i != 0:
            chunk[0] = Dateformat(chunk[0])
            if Dreamreal.objects.filter(host=chunk[1], date=chunk[0]).count() < 1:
                data.date = chunk[0]
                data.host = chunk[1]
                data.din = chunk[2]
                data.dout = chunk[3]
                data.dtot = chunk[4]
                data.save()
        i += 1


def DataValidate(hostname, date):
    try :
        datetime.datetime.strptime(date, '%m-%d-%Y').strftime('%Y-%m-%d')
        return True
    except:
        if hostname != None:
            pass
            return False


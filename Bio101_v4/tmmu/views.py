from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from django import forms
from django.template import RequestContext
import os
import random
from tmmu.models import *
from tmmu.forms import InputForm

def index(request):
    return render(request, 'tmmu/index.html')

# def upload_num(request):
#     if request.method == "POST" :
#         form = InputForm(request.POST)
#         if form.is_valid():
#             input  = form.save(commit=False)
#             results = {
#                 'value1':input.input1,
#                 'value2':input.input2,
#                 }
#             return render(request, 'igem/index.html', {'form':form, 'results':results})
#         else:
#             print form.errors
#     else:
#         form = InputForm()

#     return render(request, 'igem/index.html', {'form':form})
        

def download(request):
    the_file_name='strandardForm.xlsx' #defualt name
    filename='download.xlsx' #file path
    wrapper = FileWrapper(file(os.path.join(settings.MEDIA_ROOT, 'tmmu', filename)))
    response = StreamingHttpResponse(wrapper, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Type']='appliation/octet-stream'
    response['Content-Disposition']='attachment;filename="{0}"'.format(the_file_name)
    return response

#readfile in download
def readFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break

#upload part

#class for upload
class UploadFileForm(forms.Form):
    file = forms.FileField()
#end the def of class

dname = ''
seq = []

def handle_uploaded_file(f, path):
    newFile = f
    with open( path + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    destination.close()

def plot_img():
    choose_img=random.randint(0, 11)#b-a+1=numOfImg
    path_imgs=[
            "1.jpg",
            "2.jpg",
            "3.jpg",
            "4.jpg",
            "5.jpg",
            "6.jpg",
            "7.jpg",
            "8.jpg",
            "9.jpg",
            "10.jpg",
            "11.jpg"]

    return path_imgs[choose_img]

path_target=None

def upload_file(request):
    if request.method == 'POST' :
        uf = UploadFileForm( request.POST,request.FILES)
        if uf.is_valid():
            path =  os.path.join(settings.MEDIA_ROOT, 'tmmu', 'upload') 
            fname = request.FILES['file'].name
            dname = handle_uploaded_file(request.FILES['file'], path)
            global path_target
            path_target= plot_img()

            return render(request, 'tmmu/index.html', {'path_target':path_target})
        else:
              print form.errors
    else:
        form = UploadFileForm()
    return render(request, 'tmmu/index.html',{'form':form})


def handle_num(Nisin,Time):
    Nisin=float(Nisin)
    if Nisin <=1000:
        P=1.171-0.001*Nisin
    else:
        P=1.171-0.0012*Nisin
    
    if Time=="8_Hours":
        P=P*15/24
    return P

def upload_num(request):
    C=request.POST["Nisin"]
    T=request.POST["time"]
    Result=handle_num(C,T)    
    return render(request, 'tmmu/index.html',{'Result':Result,'path_target':path_target})

# def upload_num(request):
#     if request.method=="POST":
#         form = InputForm(request.POST)
#         if form.is_valid():
#             Nisin=request.POST.get('Nisin')
#             Time=request.POST.get('Time')
#             Result=handle_num(Nisin,Time)
#             print Result
#             return render(request, 'igem/index.html', {'Result':Result})
#         else:
#             print form.errors
#     else:
#         form=InputForm()
#     return render(request, 'igem/index.html',{'form':form})



#code from Wang
# def upload_num(request):
#     if request.method == "POST" :
#         form = InputForm(request.POST)
#         if form.is_valid():
#             input  = form.save(commit=False)
#             results = {
#                 'value1':input.input1,
#                 'value2':input.input2,
#                 }
#             return render(request, 'igem/index.html', {'form':form, 'results':results})
#         else:
#             print form.errors
#     else:
#         form = InputForm()

#     return render(request, 'igem/index.html', {'form':form})
        

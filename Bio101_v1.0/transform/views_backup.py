from django.shortcuts import render, render_to_response
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
# from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from django.conf import settings
import os
from .forms import EncodeForm 
from .forms import DecodeForm 
from .forms import EditForm
from convert.encode import encoding
from convert.decode import decoding

def index(request):
    return render(request, 'transform/index.html')

def about(request):
    return render(request, 'transform/about.html')

def edit(request):
  return render(request,'transform/edit.html') 

def encode(request):
    encode_form = EncodeForm()
    result = None
    errors = None
    if request.method == 'POST': # File Upload
       encode_form = EncodeForm(request.POST, request.FILES)
       if encode_form.is_valid():
	  stat = encode_form.save()
	  if stat:
	     result = encoding(stat.encode_file.path, stat.encode_token).result
	  else:
	     errors = "Encoding process failed."
       else:
	     errors = "Invalid information submitted."
    else:
	  encode_form = EncodeForm() # empty, unbound form

    return render(request, 'transform/encode.html', 
      	   {'encode_form':encode_form,
      	         'errors':errors,
      	        'results':result})
# def encode(request):
#     encode_form = EncodeForm()
#     result = None
#     errors = None
#     if request.method == 'POST': # File Upload
#        encode_form = EncodeForm(request.POST, request.FILES)
#        if encode_form.is_valid():
#     stat = encode_form.save()
#     if stat:
#        result = encoding(stat.encode_file.path, stat.encode_token).result
#     else:
#        errors = "Encoding process failed."
#        else:
#        errors = "Invalid information submitted."
#     else:
#     encode_form = EncodeForm() # empty, unbound form

#     return render(request, 'transform/encode.html', 
#            {'encode_form':encode_form,
#                  'errors':errors,
#                 'results':result})

def decode(request):
    decode_form = DecodeForm()
    result = None
    errors = None
    if request.method == 'POST': # File Upload
       decode_form = DecodeForm(request.POST, request.FILES)
       if decode_form.is_valid():
	  stat = decode_form.save()
	  if stat:
		 result = decoding(stat.decode_file.path, stat.decode_token).result
		 if not result:
			 result = ''
		 if os.path.isfile(result):
		    #WARNING: system dependent
		    result = '/transform/download/' + os.path.basename(result)
		 else:
		    errors ="Decoding process failed!"
		    result = None
	  else:
		 errors = "Decoding process failed."
       else:
	       errors ="Invalid information submitted."
    else:
       decode_form = DecodeForm() # empty, unbound form

    return render(request, 'transform/decode.html', 
      	   {'decode_form':decode_form,
      	         'errors':errors,
      	        'results':result})

# handling file download request
# only allow the dowloading request for the files under the MEDIA_ROOT/download
def download(request, file_name):
    wrapper = FileWrapper(file(os.path.join(settings.MEDIA_ROOT, 'download', file_name)))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    #response['Content-Length'] = 
    #response['Cache-Control'] = 
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    #response['X-Sendfile'] =
    return response

def edit(request):
  edit_form = EditForm()
  result = None
  errors = None
  if request.method == 'POST': # File Upload
    edit_form = EditForm(request.POST, request.POST)
    if edit_form.is_valid():
      stat = edit_form.save()
      if stat:
        original = stat.edit_token1
        original = original.replace('\n', '')
        original = original.replace('\r', '').split(',')
        original.remove('')
        edited = stat.edit_token2
        edited = edited.replace('\n', '')
        edited = edited.replace('\r', '').split(',')
        edited.remove('')
        def sgRNA(s):
          NTP = {'A':'U','C':'G','T':'A','G':'C'}
          sgRNA = ''
          for i in s:
            sgRNA += NTP[i]
          return sgRNA
        num = 1
        result = []
        for i in edited:
          if i not in original:
            ID = i[1:13]
            for j in original:
              if ID in j:
                mode = j[0:22]
                result.append(['original fragment'+str(num),j])
                result.append(['edited fragment'+str(num), i])
                result.append(['CRISPR sgRNA'+str(num), sgRNA(mode)])
                num = num +1
      if not result:
       result = ''
    else:
     errors = "Editing process failed."
  else:
       edit_form = EditForm() # empty, unbound form

  return render(request, 'transform/edit.html', 
           {'edit_form':edit_form,
                 'errors':errors,
                'results':result})
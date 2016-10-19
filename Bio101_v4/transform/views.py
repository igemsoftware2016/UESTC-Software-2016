from django.shortcuts import render, render_to_response
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
# from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from django.conf import settings
import os
import subprocess
from .forms import EncodeForm 
from .forms import DecodeForm
from .forms import EditForm
from convert.encode import encoding
from convert.decode import decoding
from convert.encode2 import *
from convert.decode2 import *

def index(request):
	return render(request, 'transform/index.html')

def about(request):
	return render(request, 'transform/about.html')

# def edit(request):
# 	return render(request,'transform/edit.html') 

def encode(request):
	encode_form = EncodeForm()
	result = None
	errors = None
	if request.method == 'POST': # File Upload
		encode_form = EncodeForm(request.POST, request.FILES)
		if encode_form.is_valid():
			stat = encode_form.save()
			if stat:
				method = request.POST['method']
				if method=='A':
					result = encoding(stat.encode_file.path, stat.encode_token).result
				elif method=='B':
					result = encoding2(stat.encode_file.path, stat.encode_token).result
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

def decode(request):
	decode_form = DecodeForm()
	result = None
	errors = None
	if request.method == 'POST': # File Upload
		decode_form = DecodeForm(request.POST, request.FILES)
		if decode_form.is_valid():
			stat = decode_form.save()
			if stat:
				method = request.POST['method']
				if method=='A':
					result = decoding(stat.decode_file.path, stat.decode_token).result
				elif method=='B':
					result = decoding2(stat.decode_file.path, stat.decode_token).result
                                if result: 
			        	if os.path.isfile(result):
			        		#WARNING: system dependent
			        		result = '/transform/download/' + os.path.basename(result)
				else:
					errors ="Decoding process failed!"
					result = None
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

def for_edit(s):
	if (s[0]=='C' or s[0]=='G') and (s[-1]=='A' or s[-1]=='T'):
		lis = []
		for i in s:
			lis.append(i)
		lis.reverse()
		s = ''.join(lis)
	return s[0:16], s[16:-1], s[-1]

def edit(request):
	edit_form = EditForm()
	result = None
	errors = None
	text = None
	original = None
	flag = True
	work_dir = os.path.join(settings.BASE_DIR, 'transform', 'convert')
	isnt2bit   = os.path.join(work_dir, 'isnt2bit')		# for mac os system
	if request.method == 'POST':
		edit_form = EditForm(request.POST, request.POST)
		if edit_form.is_valid():
			original = request.POST['edit_fragment']
			token = request.POST['edit_token']
			csrf = request.POST['csrfmiddlewaretoken'][0:10]
			npath = os.path.join(settings.MEDIA_ROOT, 'upload', csrf ) + '.nt'
			bpath = os.path.join(settings.MEDIA_ROOT, 'download', csrf)
			head, body, tail = for_edit(original)
			f = open(npath, 'w')
			f.write(body + '\n')
			f.close()
			subprocess.call([isnt2bit, npath, bpath, token])
			f = open(bpath, 'rb')
			text = f.read()
			f.close()
			flag = False
		else:
			edit_form = EditForm() # empty, unbound form

	return render(request, 'transform/edit.html', 
	       {'edit_form':edit_form, 'flag':flag, 'original':original, 'text': text, 'errors':errors, 'results':result})

def editted(request):
	flag = False
	text = None
	edit = None
	original = None
	xmlPath = None
	work_dir = os.path.join(settings.BASE_DIR, 'transform', 'convert')
	isbit2nt   = os.path.join(work_dir, 'isbit2nt')		# for mac os system
	if request.method == 'POST':
		csrf = request.POST['csrfmiddlewaretoken'][0:10]
		text = request.POST['edit_text']
		token = request.POST['edit_token']
		original = request.POST['original']
		bpath = os.path.join(settings.MEDIA_ROOT, 'upload', csrf )
		npath = os.path.join(settings.MEDIA_ROOT, 'download', csrf ) + '.nt'
		xmlPath = os.path.join(settings.MEDIA_ROOT, 'download', csrf ) + '.xml'
		with open(bpath, 'w') as fb:
			fb.write(text)
		subprocess.call([isbit2nt, bpath, npath, token])
		with open(npath, 'rb') as fn:
			fragment = fn.read().strip()
		edit = original[0:16] + fragment + original[-1]
		with open(os.path.join(settings.TEMPLATE_DIR, 'transform', 'sgRNA_template.rdf'), 'rb') as fm:
			temp = fm.read()
		fm.close()
		sgRNAtem = []
		for i in original[16:36]:
			sgRNAtem.append(i)
		sgRNAtem.reverse()
		with open(xmlPath, 'w') as fx:
			fx.write(temp.replace('TEMPLATESEQUENCE', ''.join(sgRNAtem)) )
		if os.path.isfile(xmlPath):
			xmlPath = '/transform/download/' + os.path.basename(xmlPath)
	else:
		edit_form = EditForm()
	return render(request, 'transform/edit.html', 
		{'flag':flag, 'text':text, 'original':original, 'edit':edit, 'xmlPath':xmlPath})

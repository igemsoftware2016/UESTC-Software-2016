#coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django import forms
import os

from handle import *
from encode.encoding import *
from decode.decoding import *
# Create your views here.
def remove():
	# delete all files in server when they reach to 500MB
	size = 0
	listpath = ['./transform/uploadFile/', './transform/blast/', './transform/decode/file/', './transform/encode/dna/']
	for path in listpath:
		for root, dirs, files in os.walk(path):  
			size += sum([os.path.getsize(os.path.join(root, name)) for name in files])  
	if size/1024/1024>500:
		for path in listpath:
			for file in os.listdir(path):
				os.remove(path + file)
		return True

def home(request):
	# when user visit home page, it will check the size of files in server, and delete them when reach 500MB
	if remove():
		print "Everything in server removed"
	return render(request, 'transform/index.html')
	
class UploadFileForm(forms.Form):
#    title = forms.CharField(max_length=50)
    file = forms.FileField()

download_path = 'transform/'
dname = ''
seq = []

def upload_encode(request):
	if request.method == 'POST':
		uf = UploadFileForm(request.POST, request.FILES)
		if uf.is_valid():
			path = 'transform/uploadFile/'

			global dname
			dname = handle_uploaded_file(request.FILES['file'], path)
			# handle_uploaded_file() return the checked name of file which uploaded by user

			token = request.POST['token']
			if not token:
				return render(request, 'transform/index.html', {'worning': 'Please input a secret code.'})

			global seq
			seq = encoding(path + dname, token).subSeq
			# start encode and encoding() return the sub sequences
			if seq:
				return render(request, 'transform/endownload.html')
	else:
		uf = UploadFileForm()
	return render(request, 'transform/index.html')
	
def endownload(request):
    def file_iterator(path, chunk_size=512):
        with open(path) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
        f.close()
    ftype = request.POST['ftype']
    fname = dname.split('.')[0]
    path = encoding_file(request, seq, fname=fname, ftype=ftype)
    # write the sub sequences into file depend on the format choosed by user
    # encoding_file() return the file path
    fname = path.split('/')[-1]		# get the sequence file name from path

    response = StreamingHttpResponse(file_iterator(path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=%s' % fname
    return response

def eblast(request):
	fname = dname.split('.')[0]
	rpath = encoding_file(request, seq, fname=fname, ftype='fasta')
	# blast must use fasta format
	fname = (rpath.split('/')[-1]).split('.')[0] + '.out'
	wpath = 'transform/blast/' + fname
	os.system('blastn -db /usr/local/ncbi/database/BIOBRICKS -query %s -out %s -outfmt 1' % (rpath, wpath))
	# blast from NCBI is installed in the server and database is from biobrick
	# -outfmt 0~9
	def file_iterator(path, chunk_size=1500):
		with open(path) as f:
			while True:
				c = f.read(chunk_size)
				if c:
					yield c
				else:
					break
		f.close()
	os.remove(rpath)
	response = StreamingHttpResponse(file_iterator(wpath))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename=%s' % fname
	return response


def upload_decode(request):
	if request.method == 'POST':
		uf = UploadFileForm(request.POST, request.FILES)
		if uf.is_valid():
			path = 'transform/uploadFile/'
			fname = handle_uploaded_file(request.FILES['file'], path)

			token = request.POST['text']
			if not token:
				return render(request, 'transform/index.html', {'worning': 'Please input your secret code.'})
			try:
				global download_path
				download_path = decoding(path=path, fname=fname, token=token).dpath
				# start decode and decoding() return the file path
				if os.path.isfile(download_path):
					return render(request, 'transform/dedownload.html')
				else:
					print download_path
					return render(request, 'transform/defail.html')
			except Exception as e:
				print e
				return render(request, 'transform/defail.html')

	else:
		uf = UploadFileForm()
	return render(request, 'transform/index.html')


def dedownload(request):
    def file_iterator(path, chunk_size=512):
        with open(path) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
        f.close()
    path = download_path
    fname = path.split('/')[-1]
    response = StreamingHttpResponse(file_iterator(path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=%s' % fname
    return response



# wpath=''
# def upload_blast(request):
# 	if request.method == 'POST':
# 		uf = UploadFileForm(request.POST, request.FILES)
# 		if uf.is_valid():
# 			path = 'transform/uploadFile/fasta/'
# 			fname = request.FILES['file'].name
# 			handle_uploaded_file(request.FILES['file'], path)

# 			rpath = path+fname
# 			global wpath
# 			wpath = 'transform/blast/' + fname.split('.')[0] + '.out'
# 			common = 'blastn -db /usr/local/ncbi/database/BIOBRICKS -query %s -out %s -outfmt 1' % (rpath, wpath)
			
# 			os.system(common)
# 			return render(request, 'transform/bldownload.html')
# 	else:
# 		uf = UploadFileForm()
# 	return render(request, 'transform/index.html')

# def bldownload(request):
# 	def file_iterator(path, chunk_size=512):
# 		with open(path) as f:
# 			while True:
# 				c = f.read(chunk_size)
# 				if c:
# 					yield c
# 				else:
# 					break
# 		f.close()
# 	path = wpath
# 	fname = path.split('/')[-1]
# 	try:
# 		response = StreamingHttpResponse(file_iterator(path))
# 	except:
# 		return render(request, 'transform/blfail.html')
# 	response['Content-Type'] = 'application/octet-stream'
# 	response['Content-Disposition'] = 'attachment;filename=%s' % fname
# 	return response

    

import os
import random

def handle_uploaded_file(f, path):
	fname = f.name.replace(' ', '')
	fname = fname.replace("'", '')
	fname = fname.replace('"', '')
	fname = fname.replace('(', '')
	fname = fname.replace(')', '')
	fname = fname.replace('/', '')
	fname = fname.replace('\\', '')
	file = path + fname
	if os.path.isfile(file):
		while os.path.isfile(file):
			fname = fname.split('.')[0] + str(random.randint(0,10)) + '.' + fname.split('.')[1]
			file = path + fname
	with open(file, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	destination.close()
	return fname

def encoding_file(request, seq, fname, ftype):
	path = 'transform/encode/dna/' + fname
	if ftype=='txt':
		f = open(path + '.' + ftype, 'w')
		for i in seq:
			f.write(i + '\n')
		f.close()



	elif ftype=='fasta':
		f = open(path + '.' + ftype, 'w')
		num = 0
		for i in seq:
			f.write('>seq:'+ str(num) + '|FILE:' + fname + '|SOFTWARE:Bio101-0.01|convert to DNA as follow.\n')
			f.write(i + '\n')
			num = num +1
		f.close()



	elif ftype=='xml':
		f = open(path + '.' + ftype, 'w')
		f.write('<?xml version="1.0" ?>\n')
		for i in seq:
			f.write('<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:prov="http://www. 29 w3.org/ns/prov#" xmlns:sbol="http://sbols.org/v2#">\n')
			f.write('\t<sbol:Sequence rdf:about="http://bio101.uestc.edu.cn/transform/">\n')
			f.write('\t\t<sbol:elements>' + i + '</sbol:elements>\n')
			f.write('\t\t<sbol:encoding rdf:resource="http://www.chem.qmul.ac.uk/iubmb/misc/naseq.html"/>\n')
			f.write('\t</sbol:Sequence>\n')
			f.write('</rdf:RDF>\n')
			f.write('\n')
		f.close()
	return path + '.' + ftype


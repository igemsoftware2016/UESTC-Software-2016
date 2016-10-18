#coding=utf-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
compress, encrypt and convert a file to DNA sequence (original full length)
convert DNA sequence to file and decrypt and decompress it
isaac64 is used to encrypt and decrypt file.
2016-9-12 pu dongkai
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from django.conf import settings
import os
import subprocess

## C-language modules and the third party program (blastn)
## WARNING: the running status by calling the foreign programs using the subprocess module
##          was not checked. 
work_dir = os.path.join(settings.BASE_DIR, 'transform', 'convert')
isaac64  = os.path.join(work_dir, 'isaac64')
bit2nt   = os.path.join(work_dir, 'bit2nt')		# for linux
isaac64  = os.path.join(work_dir, 'isaac64os')
bit2nt   = os.path.join(work_dir, 'bit2ntos')	# for mac OS
nt2bit   = os.path.join(work_dir, 'nt2bit')
# blastn   = os.path.join(work_dir, 'blastn')
# biobrick = os.path.join(work_dir, 'database', 'BIOBRICKS')


#ipath should be '"upload/" + file_name' and located under 'settings.MEDIA_ROOT'
def convert_file_to_DNA(ipath, token):
	stem = os.path.splitext(os.path.basename(ipath))[0]
	stem = os.path.join(settings.MEDIA_ROOT, 'download', stem)
	zpath = stem + '.bz2' # Compressed file
	bpath = stem + '.bit'  # Encrypted binary file
	npath = stem + '.nt'   # Converted to nt sequences
	subprocess.call(['tar', '-cjf', zpath, '-C', os.path.join(settings.MEDIA_ROOT, 'upload'), os.path.basename(ipath)])   # input file
	print ipath
	print zpath
	print bpath
	subprocess.call([isaac64, zpath, bpath, token])
	subprocess.call([bit2nt, bpath, npath])
	
	if os.path.isfile(npath):
		f = open(npath, 'r')
		seq = f.read()
		f.close
		return seq
	else:
		return None

def convert_DNA_to_file(npath, token):
	stem = os.path.splitext(os.path.basename(npath))[0]
	stem = os.path.join(settings.MEDIA_ROOT, 'download', stem)
	zpath = stem + '.bz2' # Compressed file
	bpath = stem + '.bit' # Encrypted binary file
	try:
		subprocess.call([nt2bit, npath, bpath])
		subprocess.call([isaac64, bpath, zpath, token])
		return zpath
	except:
		return ''

def int_ary(num, radix):
	result = "" 
	while num > 0:
		result = '0123456789abcdefghijklmnopqrstuvwxyz'[num % radix] + result
		num /= radix
	return result

#BLAST against BioBrick parts
def blast(in_file, out_file):
	pass
	# stat = subprocess.call([blastn, '-db', biobrick, '-query', in_file, '-out' , out_file, '-outfmt', '1'])
	# stat = subprocess.call(['gzip', '-9', out_file])
	# return stat

def RFC(in_file, out_file):
	fi = open(in_file, 'r')
	seq = fi.readlines()
	fi.close()
	# RFC10 = {'GAATTC':'EcoRI', 'TCTAGA':'XbaI', 'ACTAGT':'SpeI', 'CTGCAG':'PstI', 'GCGGCCGC':'NotI'}
	# RFC12 = {'GAATTC':'EcoRI', 'ACTAGT':'SpeI', 'GCTAGC':'NheI', 'CTGCAG':'PstI', 'GCGGCCGC':'NotI'}
	# RFC21 = {'GAATTC':'EcoRI', 'AGATCT':'BglII', 'GGATCC':'BamHI', 'CTCGAG':'XhoI'}
	# RFC23 = {'GAATTC':'EcoRI', 'TCTAGA':'XbaI', 'ACTAGT':'SpeI', 'CTGCAG':'PstI', 'GCGGCCGC':'NotI'}
	# RFC25 = {'GAATTC':'EcoRI', 'TCTAGA':'XbaI', 'GCCGGC':'NgoMIV', 'ACCGGT':'AgeI', 'ACTAGT':'SpeI', 'CTGCAG':'PstI', 'GCGGCCGC':'NotI'}
	rfc = {
	'EcoRI' : ['RFC[10]', 'RFC[12]', 'RFC[21]', 'RFC23', 'RFC[25]', 'GAATTC'],
	'XbaI' : ['RFC[10]', 'RFC23', 'RFC[25]', 'TCTAGA'],
	'SpeI' : ['RFC[10]',  'RFC[12]', 'RFC23', 'RFC[25]', 'ACTAGT'],
	'PstI' : ['RFC[10]',  'RFC[12]', 'RFC23', 'RFC[25]', 'CTGCAG'],
	'NotI' : ['RFC[10]',  'RFC[12]', 'RFC23', 'RFC[25]', 'GCGGCCGC'],
	'NheI' : ['RFC[12]', 'GCTAGC'],
	'BglII' : ['RFC[21]', 'AGATCT'],
	'BamHI' : ['RFC[21]', 'GGATCC'],
	'XhoI' : ['RFC[21]', 'CTCGAG'],
	'NgoMIV' : ['RFC[25]', 'GCCGGC'],
	'AgeI' : ['RFC[25]', 'ACCGGT'],
	}
	fo = open(out_file, 'w')
	num = 0.0
	for l in seq:
		dic = {}
		flag = False
		for enzyme in rfc.keys():
			if rfc[enzyme][-1] in l:
				flag = True
				for i in rfc[enzyme][:-1]:
					if i not in dic.keys():
						dic[i] = [['Illegal', enzyme, 'site found at:'+str(l.index(rfc[enzyme][-1])+1) ], ]
					else:
						dic[i].append(['Illegal', enzyme, 'site found at:'+ str(l.index(rfc[enzyme][-1])+1) ])
		fo.write(l)
		if flag:
			for i in dic.keys():
				num = num+1
				fo.write(i + ':\n')
				for x in dic[i]:
					for y in x:
						fo.write(y + ' ')
				fo.write('\n')
			fo.write('\n')
		else:
			fo.write('Assembly Compatibility: Compatible\n\n')
	fo.seek(0,0)
	fo.write('Assembly Compatibility rate: ' + str(round(100-(num/len(seq)*100), 0)) + '%\n')
	fo.close()



#Write sequences into Text, FASTA and SBOL formats
def write_file(path, subSeq):
	fbase = os.path.basename(path).encode('utf-8')
	stem  = os.path.splitext(fbase)[0]
	stem  = os.path.join(settings.MEDIA_ROOT, 'download', stem)
	tpath = stem + '.txt'   # Simple Text Format 
	fpath = stem + '.fasta' # FASTA Format
	xpath = stem + '.sbol'  # SBOL Format
	bpath = stem + '.log'   # Blast Report
	tf = open(tpath, 'w')
	ff = open(fpath, 'w')
	xf = open(xpath, 'w')
	#FASTA
	num = 0
	#SBOL
	xf.write('<?xml version="1.0" ?>\n')
	for i in subSeq:
		#Text
		tf.write(i + '\n')
		#FASTA
		ff.write('>seq:' + str(num) + '|FILE:' + fbase  + '|SOFTWARE:Bio101-0.01|convert to DNA as follows.\n')
		ff.write(i + '\n')
		num = num +1
		#SBOL
		xf.write('<rdf:RDF xmlns:prov="http://www.w3.org/ns/prov#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sbol="http://sbols.org/v2#" xmlns:dcterms="http://purl.org/dc/terms/">\n')
		xf.write('\t<sbol:Sequence rdf:about="http://bio101.uestc.edu.cn/">\n')
		xf.write('\t\t<sbol:elements>' + i + '</sbol:elements>\n')
		xf.write('\t\t<sbol:encoding rdf:resource="http://www.chem.qmul.ac.uk/iubmb/misc/naseq.html"/>\n')
		xf.write('\t</sbol:Sequence>\n')
		#SBOL enclosure
		xf.write('</rdf:RDF>\n')
	tf.close()
	ff.close()
	xf.close()
	# blast(fpath, bpath)
	RFC(tpath, bpath)
	#WARNING: System dependent
	stem  = '/transform/download/'+ os.path.splitext(fbase)[0]
	return { 'file_text': stem + '.txt',
		'file_fasta': stem + '.fasta',
		 'file_sbol': stem + '.sbol',
		'file_blast': stem + '.log',
		}


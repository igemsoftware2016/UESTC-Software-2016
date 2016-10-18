#coding = utf-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
decode the digital store in DNA sequences which created by Bio101 software
we used fuzzy algorithm and parity check to ensure decode information correctly
and the encrypt information is decrypt by the secret code provided by user
the information is decompressed finally
2016-9-12 pu dongkai
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
from convert import *
import re
from django.conf import settings
import subprocess
 
def reverse_s(string):
	l = []
	for i in string:
		l.append(i)
	l.reverse()
	string = ''.join(l)
	return string

def toNUM(seq): 
	dic = {
		'A':{'A':'T', 'C':'A', 'G':'C', 'T':'G'},
		'C':{'A':'G', 'C':'T', 'G':'A', 'T':'C'},
		'G':{'A':'C', 'C':'G', 'G':'T', 'T':'A'},
		'T':{'A':'A', 'C':'C', 'G':'G', 'T':'T'}}
	temp = seq[0]
	for i in range(1,len(seq)):
		temp += dic[seq[i-1]][seq[i]]
	# use the table to recover the fragment
	s = ''
	dic = {'A':'0', 'C':'1', 'G':'2', 'T':'3'}
	for i in temp:
		s += dic[i]
	# convert it to number
	return s

def file_seq(fname):
	sequence = []
	ftype = os.path.splitext(fname)[1]
	patt = re.compile('[ATCG\n]+', re.IGNORECASE)
	if ftype=='.txt':
		f = open(fname, 'r')
		for l in f.readlines():
			if not patt.match(l.strip()):
				return None
			sequence.append(l.strip())
		f.close()
	elif ftype=='.fasta':
		s = ''
		f = open(fname, 'r')
		for l in f.readlines():
			if '>' in l:
				if s:
					sequence.append(s)
					s = ''
				continue
			s += l.strip()
		if not patt.match(s):
			return None
		sequence.append(s)
		f.close()
	elif ftype=='.sbol':
		f = open(fname, 'rb')
		l = f.read()
		f.close()
		l = l.split('sbol:elements')
		for i in l:
			if 'rdf:RDF' in i:
				continue
			s = i.replace('>', '')
			s = s.replace('</', '')
			if not patt.match(s):
				return None
			sequence.append(s)
	else:
		sequence = None
	return sequence

work_dir = os.path.join(settings.BASE_DIR, 'transform', 'convert')
isnt2bit  = os.path.join(work_dir, 'isnt2bit')
def convert_to_file(npath, token):
	stem = os.path.splitext(os.path.basename(npath))[0]
	stem = os.path.join(settings.MEDIA_ROOT, 'download', stem)
	try:
		subprocess.call([isnt2bit, npath, stem, token])
		return stem
	except:
		return ''

class decoding2(object):
	def __init__(self, fname, token):
		self.Fi = {}
		seq = file_seq(fname)
		# os.remove(file)
		if seq:
			self.fragments(seq)
			npath = os.path.splitext(os.path.basename(fname))[0] + '.nt'
			npath = os.path.join(settings.MEDIA_ROOT, 'download', npath)  
			self.order(npath)
			self.result = '/media/download/' + convert_to_file(npath, token).split('/')[-1]
		else:
			self.result = None
			print "ELSE branch"


	def fragments(self, seq):
		for item in seq:
			# reverse odd fragments
			head = item[0]
			tail = item[-1]
			if (head=='C' or head=='G') and (tail=='A' or tail == 'T'):
				item = reverse_s(item)
			s = item[16:-1]		# contain file information
			P = int(toNUM(item[13]))		# check site
			index = toNUM(item[1:13])
			p = (int(index[1]) + int(index[3]) + int(index[5]) + int(index[7]) + int(index[9]) + int(index[11]))%4
			if P != p:
				continue
			i = int(index,4)
			self.Fi[i] = s

	def order(self, npath):
		fo = open(npath, 'w')
		dic = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
		for i in range(0, max(self.Fi)+1):
			if i%2==1:
				# reverse odd fragments
				s1 = []
				for dNTP in self.Fi[i]:
					s1.append(dic[dNTP])
				s1.reverse()
				fo.write(''.join(s1) + '\n')
			else:
				fo.write(self.Fi[i] + '\n')
			del(self.Fi[i])
		fo.close()








'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
file is encrypted by the secret code provided by user and compress by bz2
then convert the original DNA seuqence
split the original DNA sequence to sub DNA sequences
give each sub DNA sequence a index and check number to decode
the index is cenverted to DNA by 00 -> A, 01 -> C, 10 -> G, 11 -> T 
the sub DNA sequences is four times fold redundancy
1bit digital information is converted to 4 nucleotides
depend on the number of sub DNA sequences, we can convert file to DNA sequences with in 200MB
2016-9-12 pu dongkai
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import os
import random
from django.conf import settings
from convert import *

## 
def toDNA(s):
	lis = ['A', 'C', 'G', 'T']
	seq = ''
	for i in s:
		seq+=lis[int(i)]
	dic = {
		'A':{'A':'C', 'C':'G', 'G':'T', 'T':'A'},
		'C':{'A':'G', 'C':'T', 'G':'A', 'T':'C'},
		'G':{'A':'T', 'C':'A', 'G':'C', 'T':'G'},
		'T':{'A':'A', 'C':'C', 'G':'G', 'T':'T'}}
	temp = seq[0]
	for i in range(1,len(s)):
		temp += dic[temp[i-1]][seq[i]]
	return temp

class encoding(object):
	def __init__(self, path, token):
		self.seq = '' # Full length nt sequences
		self.S5 = ''  # with length index
		self.subSeq = [] # Fragments, split as 215 nt per fragment
		self.seq = convert_file_to_DNA(path, token)	#original DNA
		if self.seq:
			self.make_S5()		#original + S3 + S2   (50x)
			self.make_F()		# [100nt, 100nt, ]
			self.make_subSequence()		#[215nt, 215nt, ]
			self.result = write_file(path, self.subSeq)
		else:
			self.result = False

	# Prepend the length imformation, and make sequence 50x
	def make_S5(self):
		length = int_ary(len(self.seq),4)
		add = ''
		for i in range(0, 15-len(length)):	
			add += '0'
		S2 = add + length
		l = len(self.seq) + len(S2)
		len_S3 = 50 - l%50
		S3 = ''
		for i in range(0, len_S3):
			S3 += '0'
		self.S5 = self.seq + toDNA(S3) + toDNA(S2)

	# split the DNA sequence to fragmentss with 50bp per fragment
	# join four fragments to a sub sequences and make it four times-fold redundancy
	# reverse odd fragments
	def make_F(self):
		l = []
		i, ind = 0, 0
		for r in range(0, len(self.S5), 50):
			part = ''
			for x in range(0, 50):
				part += self.S5[i]
				i += 1
			l.append(part)
		for r in range(0,len(l)-3):
			s = l[r] + l[r+1] + l[r+2] + l[r+3]
			if ind%2 == 1:
				s1 = []
				for dNTP in s:
					if dNTP == "A": dNTP = "T"
					elif dNTP== "T": dNTP = "A"
					elif dNTP== "C": dNTP = "G"
					elif dNTP== "G": dNTP = "C"
					s1.append(dNTP)
				s1.reverse()
				s = ''.join(s1)
				self.subSeq.append(s)
			else:
				self.subSeq.append(s)
			ind += 1

	# add index and error-check information
	# add head and tail
	def make_subSequence(self):
		head = ['A', 'T']
		tail = ['G', 'C']
		for i in range(0, len(self.subSeq)):
			index = int_ary(i, 4)
			add = ''
			for x in range(0, 12-len(index)):		
				add += '0'
			index = add + index
			P = int(index[0]) + int(index[2]) + int(index[4]) + int(index[6]) + int(index[8]) + int(index[10])
			P = str(P%4)
			temp = self.subSeq[i] + toDNA(index) + toDNA(P)

			if temp[0] == 'A':			s = 'T' + temp
			elif temp[0] == 'T':		s = 'A' + temp
			else: s = head[random.randrange(0, 2)] + temp
			temp = s
			if temp[-1] == 'C': 		s = temp + 'G'
			elif temp[-1] == 'G':		s = temp + 'C'
			else: s = temp + tail[random.randrange(0, 2)]
			self.subSeq[i]=s

	# #Write sequences into Text, FASTA and SBOL formats
	# def write_file(self, path):
	# 	fbase = os.path.basename(path).encode('utf-8')
	# 	stem  = os.path.splitext(fbase)[0]
	# 	stem  = os.path.join(settings.MEDIA_ROOT, 'download', stem)
	# 	tpath = stem + '.txt'   # Simple Text Format 
	# 	fpath = stem + '.fasta' # FASTA Format
	# 	xpath = stem + '.sbol'  # SBOL Format
	# 	bpath = stem + '.log'   # Blast Report
	# 	tf = open(tpath, 'w')
	# 	ff = open(fpath, 'w')
	# 	xf = open(xpath, 'w')
	# 	#FASTA
	# 	num = 0
	# 	#SBOL
	# 	xf.write('<?xml version="1.0" ?>\n')
	# 	for i in self.subSeq:
	# 		#Text
	# 		tf.write(i + '\n')
	# 		#FASTA
	# 		ff.write('>seq:' + str(num) + '|FILE:' + fbase  + '|SOFTWARE:Bio101-0.01|convert to DNA as follows.\n')
	# 		ff.write(i + '\n')
	# 		num = num +1
	# 		#SBOL
	# 		xf.write('<rdf:RDF xmlns:prov="http://www.w3.org/ns/prov#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:sbol="http://sbols.org/v2#" xmlns:dcterms="http://purl.org/dc/terms/">\n')
	# 		xf.write('\t<sbol:Sequence rdf:about="http://bio101.uestc.edu.cn/">\n')
	# 		xf.write('\t\t<sbol:elements>' + i + '</sbol:elements>\n')
	# 		xf.write('\t\t<sbol:encoding rdf:resource="http://www.chem.qmul.ac.uk/iubmb/misc/naseq.html"/>\n')
	# 		xf.write('\t</sbol:Sequence>\n')
	# 		#SBOL enclosure
	# 		xf.write('</rdf:RDF>\n')
	# 	tf.close()
	# 	ff.close()
	# 	xf.close()
	# 	blast(fpath, bpath)
	# 	#WARNING: System dependent
	# 	stem  = '/transform/download/'+ os.path.splitext(fbase)[0]
	# 	return { 'file_text': stem + '.txt',
	# 		'file_fasta': stem + '.fasta',
	# 		 'file_sbol': stem + '.sbol',
	# 		'file_blast': stem + '.log.gz',
	# 		}
	

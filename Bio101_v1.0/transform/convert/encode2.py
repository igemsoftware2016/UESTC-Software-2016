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
from convert import *
from django.conf import settings
import subprocess

## C-language modules and the third party program (blastn)
## WARNING: the running status by calling the foreign programs using the subprocess module
##          was not checked. 
work_dir = os.path.join(settings.BASE_DIR, 'transform', 'convert')
isbit2nt  = os.path.join(work_dir, 'isbit2nt')

#ipath should be '"upload/" + file_name' and located under 'settings.MEDIA_ROOT'
def convert_to_DNA(ipath, token):
	stem = os.path.splitext(os.path.basename(ipath))[0]
	stem = os.path.join(settings.MEDIA_ROOT, 'download', stem)
	npath = stem + '.nt'   # Converted to nt sequences
	subprocess.call([isbit2nt, ipath, npath, token])
	if os.path.isfile(npath):
		f = open(npath, 'r')
		seq = f.readlines()
		f.close
		os.remove(ipath)
		# os.remove(npath)
		return seq
	else:
		return None

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

class encoding2(object):
	def __init__(self, path, token):
		self.subSeq = []
		seq = convert_to_DNA(path, token)	#oridinal DNA
		if seq:
			S1 = self.Index(seq)
			self.prefix_suffix(S1)
			self.result = write_file(path, self.subSeq)
		else:
			self.subSeq = False

	def Index(self, seq):
		num = 0
		S1 = []
		dic = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
		for s in seq:
			s = s.strip()
			if num%2==1:
			# reverse odd fragments
				s1 = []
				for dNTP in s:
					s1.append(dic[dNTP])
				s1.reverse()
				s = ''.join(s1)
			if s!='':
			# add index
				index = int_ary(num, 4)
				add = ''
				for x in range(0, 12-len(index)):		
					add += '0'
				index = add + index
				# fragment index
				P = int(index[1]) + int(index[3]) + int(index[5]) + int(index[7]) + int(index[9]) + int(index[11])
				# check site
				temp = toDNA(index) + toDNA(str(P%4)) + 'GG' + s
				S1.append(temp)
			num = num+1
		return S1

	def prefix_suffix(self, S1):
		for i in S1:
			head = ['A', 'T']
			tail = ['C', 'G']
			# head and tail
			if i[0] == 'A':			s = 'T' + i
			elif i[0] == 'T':		s = 'A' + i
			else: s = head[random.randrange(0, 2)] + i
			i = s
			if i[-1] == 'C': 		s = i + 'G'
			elif i[-1] == 'G':		s = i + 'C'
			else: s = i + tail[random.randrange(0, 2)]
			self.subSeq.append(s)



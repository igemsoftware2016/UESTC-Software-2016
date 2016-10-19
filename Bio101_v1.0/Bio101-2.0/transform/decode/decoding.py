#coding = utf-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
decode the digital store in DNA sequences which created by Bio101 software
we used fuzzy algorithm and parity check to ensure decode information correctly
and the encrypt information is decrypt by the secret code provided by user
the information is decompressed finally
2016-9-12 pu dongkai
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from transform.convert import *

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

	s = ''
	dic = {'A':'0', 'C':'1', 'G':'2', 'T':'3'}
	for i in temp:
		s += dic[i]
	return s

def check(dna_list, length):
	s = ''
	for i in range(0, length):
		temp = ''
		for l in dna_list:
			temp += l[i]
		A = temp.count("A")
		G = temp.count("G")
		C = temp.count("C")
		T = temp.count("T")
		maxi = max(A,G,C,T)
		if maxi==A:		s += "A"
		elif maxi==G:	s += "G"
		elif maxi==C:	s += "C"
		elif maxi==T:	s += "T"
	return s

def file_seq(file):
	sequence = []
	ftype = file.split('.')[-1]
	if ftype=='txt':
		f = open(file, 'r')
		for l in f.readlines():
			sequence.append(l.strip())
	elif ftype=='fasta':
		s = ''
		f = open(file, 'r')
		for l in f.readlines():
			if '>' in l:
				if s:
					sequence.append(s)
					s = ''
				continue
			s += l.strip()
		sequence.append(s)
		f.close()
	elif ftype=='xml':
		f = open(file, 'rb')
		l = f.read()
		f.close()
		l = l.split('sbol:elements')
		for i in l:
			if 'rdf:RDF' in i:
				continue
			s = i.replace('>', '')
			s = s.replace('</', '')
			sequence.append(s)
	else:
		return False
	return sequence

class decoding(object):
	def __init__(self, path, fname, token):
		self.sequence = ''
		self.Fi = {}
		self.F = {}
		self.S1 = ''
		file = path + fname
		self.sequence = file_seq(file)    #[115nt, ]
		os.remove(file)
		self.get_Fi()
		self.get_F()		# {0:[50nt, 50nt, 50nt, 50nt],   }
		self.get_seq()

		path = './transform/decode/file/' + fname
		f = open(path, 'w')
		f.write(self.S1)
		f.close()
		self.dpath = convert_DNA_to_file(path, token)

	# check the index
	# check the sub sequences which have the same index
	# Fi = {index: 100nt,   }
	def get_Fi(self):
		for item in self.sequence:
			if len(item)!= 215:
				continue
			head = item[0]
			tail = item[-1]
			if (head=='C' or head=='G') and (tail=='A' or tail == 'T'):
				item = reverse_s(item)
			s = item[1:201]
			P = int(toNUM(item[-2]))
			index = toNUM(item[201:213])
			p = (int(index[1]) + int(index[3]) + int(index[5]) + int(index[7]) + int(index[9]) + int(index[11]))%4
			if P != p:
				continue
			i = int(index,4)
			self.Fi[i] = s
		# 	if i not in self.Fi.keys():
		# 		self.Fi[i] = []
		# 	self.Fi[i].append(s)
		
		# for index in self.Fi.keys():
		# 	lis = self.Fi[index]
		# 	self.Fi[index] = check(lis, 200)


	# reverse odd sub sequences
	# split sub sequences to 50bp units
	# F = {index: [50bp, 50bp, 50bp, 50bp], }
	def get_F(self):
		dic = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
		for i in self.Fi.keys():
			s = self.Fi[i]
			if i%2 == 1:
				s1 = []
				s = reverse_s(s)
				for dNTP in s:
					s1.append(dic[dNTP])
				s = ''.join(s1)
			S = []
			x = 0
			while x<200:
				p = s[x: x+50]
				S.append(p)			#S = [50nt, 50nt, 50nt, 50nt ]
				x+=50
			self.F[i] = S

	# check the 50bp units
	# get the original DNA sequence length information
	# gei the original DNA sequence
	def get_seq(self):
		S5 = ''
		S5 += self.F[0][0] + self.F[0][1] + self.F[0][2]
		for i in range(0, max(self.F)+1):	# use the Four redundance
			index = [i, i+1, i+2, i+3]
			lis = []
			j = 0
			for i in index:
				try:
					lis.append(self.F[i][3-j])
					F.pop(i)
					j+=1
				except:
					j+=1
			p = check(lis, 50)		# p = 25nt
			S5 += p
		S2 = S5[len(S5)-15:]
		lenth = int(toNUM(S2), 4)
		self.S1 = S5[0: lenth]


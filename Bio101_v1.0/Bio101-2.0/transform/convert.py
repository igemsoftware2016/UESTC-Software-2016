#coding=utf-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
compress the file, encrypy and convert it to original DNA sequence
convert DNA sequence to file and decrypt and decompress it
isaac64 is used to encrypt and decrypt file.
2016-9-12 pu dongkai
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


import os
import tarfile

def convert_file_to_DNA(ipath, token):
	bzpath = ipath.split('.')[0] + '.bz2'
	bpath = bzpath.replace('bz2', 'bit')
	npath = bpath.replace('bit', 'nt')
	os.system('tar -cjf %s %s' % (bzpath, ipath))   # compressed by bzip2
	os.remove(ipath)
	os.system('./transform/isaac64 %s %s %s' % (bzpath, bpath, token))
	os.system('./transform/bit2nt %s %s' % (bpath, npath))
	if os.path.isfile(npath):
		f = open(npath, 'r')
		seq = f.read()
		f.close
		os.remove(bzpath)
		os.remove(bpath)
		os.remove(npath)
		return seq
	else:
		return False

# cause bz2 contain the path into the compressed file when encoding, so the file is stored in uploadFile when decoding
def convert_DNA_to_file(ipath, token):
	bpath = '.' + ipath.split('.')[1] + '.bit'
	bzpath = bpath.replace('bit', 'bz2')
	try:
		os.system('./transform/nt2bit %s %s' % (ipath, bpath))
		os.system('./transform/isaac64 %s %s %s' % (bpath, bzpath, token))
		with tarfile.open(bzpath, 'r:bz2') as bzf:
			name = bzf.getnames()[0]
			bzf.extract(name)
		bzf.close()
		os.remove(ipath)
		os.remove(bpath)
		os.remove(bzpath)
		return './' + name
	except:
		return 'data error'

#convert decimal system to any system within 36
def int_ary(num, radix):
	result = "" 
	while num > 0:
		result = '0123456789abcdefghijklmnopqrstuvwxyz'[num % radix] + result
		num /= radix
	return result



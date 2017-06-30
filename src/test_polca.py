import unittest
import os
import inspect
import sys

proj_dir = os.path.abspath(os.path.join(inspect.getframeinfo(inspect.currentframe()).filename, '../../'))
sys.path.append(os.path.join(proj_dir, 'src'))

data_dir = os.path.join(proj_dir, 'data')
tmp_dir = os.path.join(proj_dir, 'tmp')

if not os.path.exists(tmp_dir):
  os.mkdir(tmp_dir)

import polca

fnames_ascii = '''E.coli
a.txt
aaa.txt
alice29.txt
alphabet.txt
asyoulik.txt
bib
bible.txt
book1
book2
download.sh
fields.c
grammar.lsp
lcet10.txt
news
paper1
paper2
paper3
paper4
paper5
paper6
pi.txt
plrabn12.txt
progc
progl
progp
random.txt
world192.txt
xargs.1'''.split('\n')

fnames_binary='''geo
kennedy.xls
cp.html
obj1
obj2
sum
pic
ptt5
trans'''.split('\n')

class TestOLCA(unittest.TestCase):
  def test_binary_file(self):
    files = [os.path.join(data_dir, fname) for fname in fnames_ascii + fnames_binary]
    for in_fname in files:
      print('test: {}'.format(in_fname))
      with open(in_fname, 'rb') as input:
        enc_fname = os.path.join(tmp_dir, '{}.enc'.format(os.path.basename(in_fname)))
        decomp_fname = os.path.join(tmp_dir, '{}.decomp'.format(os.path.basename(in_fname)))
        with open(enc_fname, 'w') as output:
          polca.compress(input, output)
      with open(enc_fname, 'r') as input:
        with open(decomp_fname, 'wb') as output:
          polca.decompress(input, output)
      with open(in_fname, 'rb') as input:
        file_str = input.read()
      with open(decomp_fname, 'rb') as input:
        decomp_str = input.read()
      self.assertEqual(file_str, decomp_str)

  def test_text_file(self):
    files = [os.path.join(data_dir, fname) for fname in fnames_ascii]
    for in_fname in files:
      print('test: {}'.format(in_fname))
      with open(in_fname, 'r') as input:
        enc_fname = os.path.join(tmp_dir, '{}.enc'.format(os.path.basename(in_fname)))
        decomp_fname = os.path.join(tmp_dir, '{}.decomp'.format(os.path.basename(in_fname)))
        with open(enc_fname, 'w') as output:
          polca.compress(input, output)
      with open(enc_fname, 'r') as input:
        with open(decomp_fname, 'w') as output:
          polca.decompress(input, output)
      with open(in_fname, 'r') as input:
        file_str = input.read()
      with open(decomp_fname, 'r') as input:
        decomp_str = input.read()
      self.assertEqual(file_str, decomp_str)

if __name__=='__main__':
  unittest.main()
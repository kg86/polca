# POLCA

**P**ython implementation of the online grammar compression algorithm **OLCA**.
POLCA was developed for studying OLCA, so its time and space  consumption and the output compressed size are much worse than [lcacomp](http://code.google.com/p/lcacomp/) which is a C++ implemenation of OLCA.
However, POLCA has an advantage, lcacomp does not have, that it can treat each multi byte character as a single character.

**Note:** The main drawback of POLCA is that it stores each whole line of input in RAM because python does not provide an interface for reading by characters.

## Requirements

Python 3.5 or higher is required.
See `requirements.txt` for other required libraries.
They will be installed by the following command.

```sh
$ pip install -r requirements.txt
```

## Usages

```sh
$ python src/polcarun.py -h
src/polcarun.py: Python implementation of the online grammar compression algorithm OLCA.

Usage:
  src/polcarun.py (comp | decomp) [options]
  
Options:
  -i FILE --input FILE              input file  [default: stdin]
  -o FILE --output FILE             output file [default: stdout]
  -e ENCODING --encoding ENCODING   open input/output by ENCODING for comp/decomp [default: binary]
                                    if ENCODING="binary", treat a byte as a single character 
                                    otherwise, treat a multi-byte encoded by ENCODING as a single character
```

## Examples

An example for a small text.

```sh
$ echo "hogehoge" > hoge.txt
$ python src/polcarun.py comp -i hoge.txt -o hoge.enc
$ python src/polcarun.py decomp -i hoge.enc -o hoge.decomp
$ cat hoge.decomp
hogehoge
```

An example for a highly-repetitive text.
**Note:** The compressed size is very small, but POLCA store whole input (about 17M) in RAM.
This is because the input huge data is written in a line.

```sh
$ python -c "print('a'*(2**24))" > fuga.txt # 16777217 bytes (about 17M)
$ python src/polcarun.py comp -i fuga.txt -o fuga.enc # 266 bytes
$ python src/polcarun.py comp -i fuga.enc -o fuga.decomp
$ diff fuga.txt fuga.decomp
# no output
```

An example for a multi-byte text.

```sh
$ echo "âêîôû" | python src/polcarun.py comp --encoding=utf8 | python src/olcamain.py decomp --encoding=utf8
âêîôû
# ofcourse, you can treat a byte as a character also for a multi-byte text!
$ echo "âêîôû" | python src/polcarun.py comp | python src/olcamain.py decomp
âêîôû
```

## Tests

```sh
$ cd download
$ ./download.sh # download corpus
$ cd ../
$ python -m unittest -v src/test_polca.py
```

`download.sh` downloads files for test from [The Canterbury Corpus](http://corpus.canterbury.ac.nz/purpose.html).

## Licenses

MIT © 2017 Keisuke Goto

## References

- Shirou Maruyama, Hiroshi Sakamoto, Masayuki Takeda: An Online Algorithm for Lightweight Grammar-Based Compression. Algorithms 5(2): 214-235 (2012)
- [lcacomp](http://code.google.com/p/lcacomp/): A C++ implementation of OLCA.
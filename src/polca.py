import sys
import io
from slp import DynamicSLP, SLPIO

class POLCA:
  QSIZE = 5
  def __init__(self):
    self.slp = DynamicSLP()
    self.queues = []
    self.text_len = 0

  @staticmethod
  def lca(i, j):
    return (i ^ j).bit_length()

  @staticmethod
  def _is_replaced_pair(queue, i):
    def isMin(j):
      return queue[j-1] > queue[j] < queue[j+1]
    def isLCAmax(j):
      return POLCA.lca(queue[j - 1], queue[j]) < POLCA.lca(queue[j], queue[j + 1]) > POLCA.lca(queue[j + 1], queue[j + 2])
    if queue[i] == queue[i+1]:
      return True
    elif queue[i + 1] == queue[i + 2]:
      return False
    elif queue[i + 2] == queue[i + 3]:
      return True
    elif isMin(i) or isLCAmax(i):
      return True
    elif isMin(i+1) or isLCAmax(i+1):
      return False
    else:
      return True

  def _insert_queue(self, c, stage):
    if len(self.queues) <= stage:
      self.queues.append([sys.maxsize])
    q = self.queues[stage]
    q.append(c)

    if len(q) >= POLCA.QSIZE:
      if POLCA._is_replaced_pair(q, 1):
        self._insert_queue(self.slp.invOrCreate(q[1], q[2]), stage + 1)
        q.pop(0)
        q.pop(0)
      else:
        self._insert_queue(q[1], stage + 1)
        q.pop(0)

  def append(self, c):
    self.text_len += 1
    self._insert_queue(self.slp.invCharOrCreate(c), 0)

  def flush(self):
    while len(self.queues) >= 1:
      q = self.queues[0]
      if len(q) == 2:
        if len(self.queues) > 1:
          self._insert_queue(q[1], 1)
        self.queues.pop(0)
      else:
        self._insert_queue(self.slp.invOrCreate(q[1], q[2]), 1)
        q.pop(0)
        q.pop(0)
        if len(q) == 1:
          self.queues.pop(0)

def compress(input, output):
  olca = POLCA()
  for line in input:
    for c in line:
      olca.append(c)
  olca.flush()
  olca.slp.setInfo(olca.text_len)

  SLPIO.encode(olca.slp, output)

def decompress(input, output):
  encode = (lambda c: c.to_bytes(1, 'little')) if isinstance(output, io.BufferedWriter) else (lambda c: c)
  slp = SLPIO.decode(input)
  for c in slp:
    output.write(encode(c))
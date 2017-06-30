import json

class SLP:
  _char_index = 0
  def __init__(self, vars = None):
    self._vars = vars if vars else [(0, 0)]

  def __len__(self):
    return len(self._vars)

  def __iter__(self):
    return SLPgen(self)

  def left(self, i):
    return self._vars[i][0]

  def right(self, i):
    return self._vars[i][1]

  def char(self, i):
    return self.right(i)

  def isChar(self, i):
    return self.left(i) == SLP._char_index

def SLPgen(slp, root=None):
  stack = [root if root else len(slp) - 1]
  while len(stack) > 0:
    x = stack.pop(len(stack)-1)
    if slp.isChar(x):
      yield slp.char(x)
    else:
      stack.append(slp.right(x))
      stack.append(slp.left(x))

class SLPIO:
  @staticmethod
  def encode(slp, fp):
    fp.write(json.dumps(slp._vars, ensure_ascii=False))

  @staticmethod
  def decode(fp):
    return SLP(json.load(fp))

class DynamicSLP(SLP):
  def __init__(self, vars=None):
    super().__init__(vars)
    self._inv = dict(((l, r), i) for i, (l, r) in enumerate(self._vars[1:]))

  def addVar(self, l, r):
    self._vars.append((l, r))
    self._inv[(l, r)] = len(self._vars) - 1
    return len(self._vars) - 1

  def addChar(self, c):
    return self.addVar(SLP._char_index, c)

  def hasVar(self, l, r):
    return (l, r) in self._inv

  def hasChar(self, c):
    return self.hasVar(SLP._char_index, c)

  def inv(self, l, r):
    return self._inv[(l, r)]

  def invOrCreate(self, l, r):
    '''return index i s.t. Xi = Xl Xr (create a new variable if such i does not exist) 
    '''
    if not self.hasVar(l, r):
      return self.addVar(l, r)
    return self._inv[(l, r)]

  def invChar(self, c):
    return self._inv[(SLP._char_index, c)]

  def invCharOrCreate(self, c):
    '''return index i s.t. Xi = c (create a new variable if such i does not exist) 
    '''
    if not self.hasChar(c):
      return self.addChar(c)
    return self.invChar(c)

  def setInfo(self, text_len=None):
    self._vars[0] = (text_len if text_len else sum(1 for _ in self), len(self)) # (length of original text, size of slp)
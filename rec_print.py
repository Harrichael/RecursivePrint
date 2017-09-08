from collections import defaultdict

class RecursivePrint(object):
  def __init__(self, func):
    self.func = func
    self.call_depth = 0
    self.call_id_counter = -1
    self.parent_call_id_stack = [-1]
    self.children = defaultdict(list)
    self.args = {}
    self.ret = {}

  def __call__(self, *args):
    self.call_depth += 1
    parent_call_id = self.parent_call_id_stack[-1]
  
    self.call_id_counter += 1
    call_id = self.call_id_counter
    self.args[call_id] = list(args)
    self.children[parent_call_id].append(call_id)
    self.parent_call_id_stack.append(call_id)
    
    retVal = self.func(*args)
    self.ret[call_id] = retVal

    self.parent_call_id_stack.pop()
    self.call_depth -= 1
    if self.call_depth == 0:
      self.print_children()
      self.__init__(self.func)

    return retVal

  def create_node_text(self, call_ids, retVal, debug=None):
    if debug is None:
      debug = ''
    else:
      debug = ', debug=' + str(debug)
    return '{name}({args}{debug})={ret}'.format(
      name=self.func.__name__,
      args=','.join(map(str, call_ids)),
      ret=retVal,
      debug=debug,
    )

  def print_children(self):
    frontier = [(0, 0)]
    while frontier:
      node, depth = frontier[-1]
      del frontier[-1]
      frontier.extend(map(lambda n: (n, depth+1), self.children[node]))
      node_print( self.create_node_text( self.args[node], self.ret[node] ), depth )
    
def node_print(text, level):
  print('\t'*level + str(text))

@RecursivePrint
def fibo_pairs(n):
    if n == 0:
        return (0, 1)
    elif n > 0:
        prev_1, prev_2 = fibo_pairs(n-1)
        return prev_1 + prev_2, prev_1
    else:
        prev_1, prev_2 = fibo_pairs(n+1)
        if prev_2 > 0:
            return (abs(prev_1) + abs(prev_2)), prev_1
        else:
            return -(abs(prev_1) + abs(prev_2)), prev_1
            


def fibonacci_1(n):  
    return fibo_pairs(n)[0]

@RecursivePrint
def fibonacci_2(n):  
    if n <= 2: 
        return 1
    else:
        return fibonacci_2(n-1) + fibonacci_2(n-2)

if __name__ == '__main__':
  fibonacci_2(9)
  fibonacci_1(-9)

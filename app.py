from MCTS.oracle import Oracle
from MCTS.oracle import OracleRPN
from MCTS.mcts import MCTS
import time

#dataset = OracleRPN.dataset()
dataset = Oracle.dataset()


mcts = MCTS(['!', '~'], ["+", "-", "*", "&", "|", "^"] ,["a", "b", "c"], dataset)
#mcts = MCTS([], ["+", "-", "*", "&", "|", "^"] ,["a", "b", "c"], dataset)
start_time = time.time()
count = 0
while count < 1000000 and not mcts.iterate():
    count += 1
    if count % 1000 == 0:
        print(count)

print(count)
print("--- %s seconds ---" % (time.time() - start_time))

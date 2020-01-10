from MCTS.oracle import Oracle
from MCTS.mcts import MCTS

dataset = Oracle.dataset()

#mcts = MCTS([],["+", "-", "*", "&", "|", "^"] ,["a", "b"], dataset)
mcts = MCTS([],["+", "-", "*"] ,["a", "b", "c"], dataset)
#mcts = MCTS([],["+", "-"] ,["a", "b"], dataset)

count = 0
while count < 10000 and not mcts.iterate():
    count += 1
    if count % 100 == 0:
        print(count)

print(count)
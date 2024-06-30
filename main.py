from afd import AFD
from afnd import AFND

afd = AFD()
afd.fromFile('input.txt')
#afnd.printStates()
afd.printWithError()

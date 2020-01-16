#完成一个短序列的组装
import re
import itertools
from collections import defaultdict
#读fasta文件，将每一个read加入列表
seq=[]
with open("Assembleliu.fa",'r') as fasta:
    for line in fasta.readlines():
        if line.startswith('>'):
            continue
        else:
            #先通过正则表达式去除其他的字符
            line = re.sub('[^ATCGatcg]','',line)
            seq.append(line)

#下面来进行拼接,这部分代码来自于课件

def overlap(a, b, min_length=3):
    """Return length of longest suffix of 'a'.
    function matches a prefix of 'b' that is at least 'min_length'
    characters long.  If no such overlap exists,
    return 0.
    """
    start = 0  # start all the way at the left
    while True:
        start = a.find(b[:min_length], start)  # look for b's suffx in a
        if start == -1:  # no more occurrences to right
            return 0
        # found occurrence; check for full suffix/prefix match
        if b.startswith(a[start:]):
            return len(a)-start
        start += 1  # move just past previous match


def scs(ss):
    """Return shortest common superstring."""
    shortest_sup = None
    for ssperm in itertools.permutations(ss):
        sup = ssperm[0]  # superstring starts as first string
        for i in range(len(ss)-1):
            # overlap adjacent strings A and B in the permutation
            olen = overlap(ssperm[i], ssperm[i+1], min_length=1)
            # add non-overlapping portion of B to superstring
            sup += ssperm[i+1][olen:]
        if shortest_sup is None or len(sup) < len(shortest_sup):
            shortest_sup = sup  # found shorter superstring
    return shortest_sup  # return shortest



#输出结果
print("SCS result: ", scs(seq))
print("SCS length: ", len(scs(seq)))
#比较SCS length 和题目中给出的长度可以判断是否为ciucle,如果是circle,
# 那么SCS result给出的结果就并不可靠，由于我自己作业是线性的，就不管怎么输出circle了[->_->]

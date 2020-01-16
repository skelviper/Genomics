genomeSeq = ""
with open("./GenomeKmerDepth.fa",'r') as genome:
    for line in genome.readlines():
        if line.startswith('>'):
            continue
        if (line == '\n'):
            continue
        else:
            line.rstrip();
            genomeSeq += line

#遇到新的kmer加入字典，遇到已经有的就在字典里加入新的键值对
genomeSeq =genomeSeq.rstrip()
k = 3
dictKmer = {}
total = 0
i = 0#字符串标记
while (i<len(genomeSeq)-k):
    tempMer = genomeSeq[i:i+k]
    #print(tempMer)
    if tempMer in dictKmer:
        dictKmer[tempMer] +=1
        total +=1
    else:
        dictKmer[tempMer] = 1
        total +=1
    i+=1
    

#输出出现最多的kmer
output = sorted(dictKmer.items(),key = lambda item:item[1])
print(output[-1])



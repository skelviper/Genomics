#Genomics Homework4 
#Use DP algorithm to find the highest scored alignment
#1. Calculate the alignment score of seq1&seq2
#2. find the best alignment
#3. Calculate the best alignment score 

seq1 = "ACGCNCTTTTCTCGCGTACCTTTACTAATAGAATGCAAAGACGTCCCCCG"
seq2 = "CTCGCGTACCTTTACTAAGAGAATGCGNAGACGTCCCCCGGNGGACCGAT"

match_award = 1
mismatch_penalty = -2
N = -1
gap_penalty = -3
Extendgap_recalibration = 1 #延伸gap的罚分是-2，检测到上一个来自于上方向或者左方向，就给gap_penalty+1

def alignScore(seq1,seq2):
    score =0
    for i,j in zip(seq1,seq2):
        if(i == "N" or j == "N"):
            score -=1
        elif (i == "-" or j =="-"):
            score -= 2
        elif (i == j):
            score +=1
        else :
            score -=2 #mismatch
    return score

# 初始化打分表
def zeros(shape):
    retval = []
    for x in range(shape[0]):
        retval.append([])
        for y in range(shape[1]):
            retval[-1].append(0)
    return retval

# 计算得分
def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == 'N' or beta == 'N':
        return N
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty

def water(seq1, seq2):
    m, n = len(seq1), len(seq2)  # length of two sequences

    # Generate DP table and traceback path pointer matrix
    score = zeros((m+1, n+1))      # the DP table
    pointer = zeros((m+1, n+1))    # to store the traceback path

    max_score = 0        # initial maximum score in DP table

    # Calculate DP table and mark pointers
    for i in range(1, m + 1):
        for j in range(1, n + 1):#第一行第一列都是0，所以循环从1开始。
            score_diagonal = score[i-1][j-1] + match_score(seq1[i-1], seq2[j-1])
            #填充的格子从1开始，填充格子的1对应序列的0，所以match_score的下表要减去1
            score_up = score[i][j-1] + gap_penalty
            score_left = score[i-1][j] + gap_penalty

            if (pointer[i][j-1] == ( 2)):
                score_up = score[i][j-1] + gap_penalty + Extendgap_recalibration
            if (pointer[i-1][j] == (1 )):
                score_left = score[i-1][j] + gap_penalty + Extendgap_recalibration

            score[i][j] = max(0,score_left, score_up, score_diagonal)

            if score[i][j] == 0:
                pointer[i][j] = 0 # 0 means end of the path
            if score[i][j] == score_left:
                pointer[i][j] = 1 # 1 means trace up
            if score[i][j] == score_up:
                pointer[i][j] = 2 # 2 means trace left
            if score[i][j] == score_diagonal:
                pointer[i][j] = 3 # 3 means trace diagonal
            if score[i][j] >= max_score:
                max_i = i
                max_j = j
                max_score = score[i][j]

    align1, align2 = '', ''    # initial sequences

    i,j = max_i,max_j    # indices of path starting point

    #traceback, follow pointers
    while pointer[i][j] != 0:
        if pointer[i][j] == 3:
            align1 += seq1[i-1]
            align2 += seq2[j-1]
            i -= 1
            j -= 1
        elif pointer[i][j] == 2:
            align1 += '-'
            align2 += seq2[j-1]
            j -= 1
        elif pointer[i][j] == 1:
            align1 += seq1[i-1]
            align2 += '-'
            i -= 1
    #[align1,align2,symbol,maxscore] 
    answerlist= finalize(align1, align2)
    answerlist.append(max_score)
    return answerlist

def finalize(align1, align2):
    align1 = align1[::-1]    #reverse sequence 1
    align2 = align2[::-1]    #reverse sequence 2

    i,j = 0,0

    #输出结果: alignment 
    symbol = ''
    identity = 0
    for i in range(0,len(align1)):
        # if two AAs are the same, then output the letter
        if (align1[i] == align2[i]):                
            symbol += "*"
        # if one of them is N
        elif (align1[i] =="N" or align2[i]=="N"):
            symbol += "N"
        # if they are not identical and none of them is gap
        elif (align1[i] != align2[i] and align1[i] != '-' and align2[i] != '-'): 
            symbol += 'M'
        #if one of them is a gap, output a -
        elif (align1[i] == '-' or align2[i] == '-'):          
            symbol += '-'

    return[align1,align2,symbol]

def printer(answerlist):
    #answerlist: [align1,align2,symbol,maxscore]
    print("seq1 " + answerlist[0])
    print("seq2 " + answerlist[1])
    print("symb " + answerlist[2])
    print("Best Alignment score: " + str(answerlist[3]))


print("Alignment socre: " + str(alignScore(seq1,seq2)))
printer(water(seq1,seq2))
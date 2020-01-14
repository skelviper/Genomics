# 解决hw3中的第一题

# 计算当前序列的概率，结果用lg表示

# veterbi函数输出最大可能性的路径和概率值
import math
import csv  # 用来写tsv文件
import numpy as np
from decimal import Decimal
# 强制保留两位小数

states = ('E', '5', 'I', '3')

# 把自己的序列贴到observation这里，我懒得写读取字符串了
observations = "ATTGAACTGAGCACCTGGGAGGCAAAAAATGGGGAACGTCGAAACCATCCGTTCTAGCAACATATTTCTACTAAAAAATGCTTGCTGAATGTTATTAGCCGGACCTTCTCCCCACAGCACACCTTGTTAAGTAAATCTTAACTAAAATTTGAAGATTAAGAACCACAGTTTCATAAGGGCGAGGTGGAATCTTTCGCGCGCGGGGTAGTTTCCTACGGTGGATAGTCCTGGCAGTAGTGCGAAGGGAGTTATCGTACAACCCACGACCGAAGGGGTGACTAGCCTACGTTGTACTACCTTTTAGTTGGGATTAATTACCTTCAGAGACATCTTTCATAGCAAAAATGTTGCGGAATTACATCGAGAGTCGACAGTCTTTCATACTGATTTCCTC"
# 观察到的，我们需要根据这个和那些概率信息输出各个观察到的状态实际是什么


start_probability = {'E': 1, '5': 0, 'I': 0, '3': 0}

transition_probability = {
    'E': {'E': 0.9, '5': 0.1, 'I': 0, '3': 0},
    '5': {'E': 0, '5': 0, 'I': 1, '3': 0},
    'I': {'E': 0, '5': 0, 'I': 0.9, '3': 0.1},
    '3': {'E': 1, '5': 0, 'I': 0, '3': 0},
}

emission_probability = {
    'E': {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25},
    '5': {'A': 0.05, 'C': 0.00, 'G': 0.95, 'T': 0.00},
    'I': {'A': 0.40, 'C': 0.10, 'G': 0.10, 'T': 0.40},
    '3': {'A': 0.00, 'C': 0.05, 'G': 0.95, 'T': 0.00},
}


def writeTSV1(matrix):
    with open('./output/MaxProbMatrix.tsv', 'w', newline='') as out_file:
        # 这个写法是为了防止输出的文件中被蜜汁添加回车
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['Indx', 'E', '5', 'I', '3'])
        i = 1
        for line in matrix:
            tsv_writer.writerow([i, '%.2f' % np.log10(line['E']), '%.2f' % np.log10(
                line['5']), '%.2f' % np.log10(line['I']), '%.2f' % np.log10(line['3'])])
            # math 库自带的log是无法处理log10(0)的，而使用numpy的log10 可以得到inf
            i += 1

# 下面这两个函数是辅助writeTSV2的


def ifZero(line, n):
    if line[n] != 0:
        return n
    else:
        return '-'


def lineMax(line):
    (prob, state) = max([(line[y], y) for y in states])
    return state


def writeTSV2(matrix, str):
    # 下面来写pointer matrix文件
    with open('./output/PrinterMatrix.tsv', 'w', newline='') as out_file2:
        tsv_writer2 = csv.writer(out_file2, delimiter='\t')
        tsv_writer2.writerow(['Indx', 'E', '5', 'I', '3', 'State'])
        i = 1
        for line in matrix:
            row = [i, line['E'][-1], line['5'][-1], line['I'][-1], line['3']]
            row.append(str[i-1])
            tsv_writer2.writerow(row)
            i += 1
    print("Done wrote tsv")


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]  # dict in list
    path = {}  # path is a dict
    pointer = [{}]

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
        pointer[0][y] = '-'

    # Run Viterbi for t > 0
    i = 1
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
        pointer.append({})
        for y in states:
            (prob, state) = max(
                [(V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states])
            # 怎样取出这个最大的y0？

            # 只取这一步骤下概率最大的
            V[t][y] = prob
            if (prob != 0):
                pointer[t][y] = path[state][-1]
            else:
                pointer[t][y] = '-'

            newpath[y] = path[state] + [y]

        i += 1

        # Don't need to remember the old paths

        path = newpath

    (prob, state) = max([(V[len(obs) - 1][y], y)
                         for y in states])  # 字典中最后一行最大概率的
    str_out = "".join(path[state])

    writeTSV1(V)
    writeTSV2(pointer, str_out)

    return (round(math.log10(prob), 2), str_out)


def main():
    return viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)


print(main())

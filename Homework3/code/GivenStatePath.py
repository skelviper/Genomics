import math

states = ('E','5','I','3')

#把自己的序列贴到observation这里，我懒得写读取字符串了

givenLable = "EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE5IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII3EEEEEEEEEEEEEEEEEE5IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII3EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
observations = "TTCATATTATGCAGAAAATCTACTTCGCCTGATACGAGTCGGTTATCTTCGGATACTGTATAGTCCCACCTGGTGATCCTATGCTGTACAATTTATATTACAAAATATGATAATAAGATTCAGGTAAGCGAGCTACATCACTTCTCGTAAAAGCTATCTAAAATATAATAATACATAAGTTATAAAAATAATTTTAAAAGAAACCCCGGGGGGAGCTCAGATATCCGATACAGGGATGAAGAAATAACCTCATCCCATTGGTGACGAAAGGTTGTAAGTAGCTGGCCGCCGAGATAGCTGAGCGGCGAACCACTAGA" 
#观察到的，我们需要根据这个和那些概率信息输出各个观察到的状态实际是什么

 
start_probability = {'E':1,'5':0,'I':0,'3':0}
 
transition_probability = {
   'E' : {'E': 0.9, '5': 0.1,'I':0,'3':0},
   '5' : {'E': 0, '5': 0,'I':1,'3':0},
   'I' : {'E': 0, '5': 0,'I':0.9,'3':0.1},
   '3' : {'E': 1, '5': 0,'I':0,'3':0},
   }
 
emission_probability = {
   'E' : {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T':0.25},
   '5' : {'A': 0.05, 'C': 0.00, 'G': 0.95, 'T':0.00},
   'I' : {'A': 0.40, 'C': 0.10, 'G': 0.10, 'T':0.40},
   '3' : {'A': 0.00, 'C': 0.05, 'G': 0.95, 'T':0.00},
   }

probability = 0.25 
#初始概率，一定是外显子概率1，乘以四种情况的0.25，这里我偷懒直接填上去了

for i in range(1,len(givenLable)):
    probability = probability * transition_probability[givenLable[i-1]][givenLable[i]] * emission_probability[givenLable[i]][observations[i]]

print(round(math.log10(probability),2))

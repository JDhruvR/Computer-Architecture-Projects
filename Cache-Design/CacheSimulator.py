import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
from tabulate import tabulate

class Cache:
    def __init__(self, cacheSize:int, accesses:str, blockSize:int, wayCount:int): #Initializes a new cache with a dictionary.
        # index : [[valid, tag, LRU bit],[..],[..].. no of blocks for each index. i.e ways]
        #id=[i for i in range(lines)]
        #cacheBlocks=[[[0, '', 0] for i in range(4)] for j in range(lines)]
        self.lines=int(((cacheSize*1024)/blockSize)/wayCount)
        self.instructionFileName=accesses
        self.blockSize=blockSize
        self.cacheDict=dict(zip([i for i in range(self.lines)], [[[0, 0, 0] for i in range(wayCount)] for j in range(self.lines)])) #initialize with all 0s.
        self.hitCount=0
        self.missCount=0
        self.accessCount=0

        self.hitPlot=[]
        self.missPlot=[]
        self.accessPlot=[]

        with open(accesses, 'r') as file:
            for line in file:
                parts = line.strip().split()
                address = parts[1]
                binAddress=bin(int(address, 16))[2:]

                if(len(binAddress)!=32):
                    binAddress=('0'*(32-len(binAddress)))+binAddress

                byteOffset=int(math.log(blockSize, 2))
                indexLength=int(math.log(self.lines, 2))
                tagLength=32-byteOffset-indexLength

                self.cacheAccess(int(binAddress[0:tagLength], 2), int(binAddress[tagLength:tagLength+indexLength], 2))

                self.hitPlot.append(self.hitCount)
                self.missPlot.append(self.missCount)
                self.accessPlot.append(self.accessCount)

        self.hit_miss_rate=(self.hitCount/self.missCount)
        self.hit_rate=(self.hitCount/self.accessCount)*100
        self.miss_rate=(self.missCount/self.accessCount)*100

    def cacheAccess(self, tag:int, id:int):
        for block in self.cacheDict[id]:
            if (block[0]==1 and block[1]==tag): # Cache Hit has happened.
                self.hitCount+=1
                self.accessCount+=1

                for otherBlocks in self.cacheDict[id]:
                    if (otherBlocks[0]==1 and otherBlocks[2]<block[2]):
                        otherBlocks[2]+=1

                block[2]=1
                return

        #Cache hit hasnt happened and hence we call the cacheMiss method to do the needfull.
        self.cacheMiss(tag, id)
        return

    def cacheMiss(self, tag:int, id:int):
        self.missCount+=1
        self.accessCount+=1

        for block in self.cacheDict[id]:
            if(block[0]==0):
                for otherBlocks in self.cacheDict[id]:
                    if otherBlocks[0]==1:
                        otherBlocks[2]+=1

                block[0]=1
                block[1]=tag
                block[2]=1
                return

        for block in self.cacheDict[id]:
            if block[2]==len(self.cacheDict[id]):
                for otherBlocks in self.cacheDict[id]:
                    otherBlocks[2]+=1

                block[1]=tag
                block[2]=1
                return

############################## Question Part (A) ##############################
# Design a 4-way SA Cache with blockSize=4bytes and input is of 32 bits.
# Note: We input the lines and not the size of the cache in kB. the unit of blockSize is in Bytes.

df_A = pd.DataFrame(index=['gcc', 'gzip', 'mcf', 'swim', 'twolf'])
def QuestionA():
    cache1=Cache(cacheSize = 1024, accesses='traces/gcc.trace', blockSize=4, wayCount=4)
    cache2=Cache(cacheSize = 1024, accesses='traces/gzip.trace', blockSize=4, wayCount=4)
    cache3=Cache(cacheSize = 1024, accesses='traces/mcf.trace', blockSize=4, wayCount=4)
    cache4=Cache(cacheSize = 1024, accesses='traces/swim.trace', blockSize=4, wayCount=4)
    cache5=Cache(cacheSize = 1024, accesses='traces/twolf.trace', blockSize=4, wayCount=4)

    result_hit_rate = {
        'gcc': cache1.hit_rate,
        'gzip': cache2.hit_rate,
        'mcf': cache3.hit_rate,
        'swim': cache4.hit_rate,
        'twolf': cache5.hit_rate
    }

    result_miss_rate = {
        'gcc': cache1.miss_rate,
        'gzip': cache2.miss_rate,
        'mcf': cache3.miss_rate,
        'swim': cache4.miss_rate,
        'twolf': cache5.miss_rate
    }

    result_hit_miss_rate = {
        'gcc': cache1.hit_miss_rate,
        'gzip': cache2.hit_miss_rate,
        'mcf': cache3.hit_miss_rate,
        'swim': cache4.hit_miss_rate,
        'twolf': cache5.hit_miss_rate
    }

    df_A['Hit Rate'] = result_hit_rate
    df_A['Miss Rate'] = result_miss_rate
    df_A['Hit/Miss Ratio'] = result_hit_miss_rate
    
    print("Answer to Question A: ")
    print("These are the hit rate, miss rate and Hit/Miss Ratio for the given Cache.\n")
    print(tabulate(df_A, headers='keys', tablefmt='grid'))
    print("\n")

###############################################################################

############################## Question Part (B) ##############################

df_B_HitRate = pd.DataFrame(index=['gcc', 'gzip', 'mcf', 'swim', 'twolf'])
df_B_MissRate = pd.DataFrame(index=['gcc', 'gzip', 'mcf', 'swim', 'twolf'])
df_B_HitMissRate = pd.DataFrame(index=['gcc', 'gzip', 'mcf', 'swim', 'twolf'])

def QuestionB():
    #for 128kB Cache:
    cache_128_1=Cache(cacheSize=128, accesses='traces/gcc.trace', blockSize=4, wayCount=4)
    cache_128_2=Cache(cacheSize=128, accesses='traces/gzip.trace', blockSize=4, wayCount=4)
    cache_128_3=Cache(cacheSize=128, accesses='traces/mcf.trace', blockSize=4, wayCount=4)
    cache_128_4=Cache(cacheSize=128, accesses='traces/swim.trace', blockSize=4, wayCount=4)
    cache_128_5=Cache(cacheSize=128, accesses='traces/twolf.trace', blockSize=4, wayCount=4)

    result_128_hit_rate = {
        'gcc': cache_128_1.hit_rate,
        'gzip': cache_128_2.hit_rate,
        'mcf': cache_128_3.hit_rate,
        'swim': cache_128_4.hit_rate,
        'twolf': cache_128_5.hit_rate
    }

    result_128_miss_rate = {
        'gcc': cache_128_1.miss_rate,
        'gzip': cache_128_2.miss_rate,
        'mcf': cache_128_3.miss_rate,
        'swim': cache_128_4.miss_rate,
        'twolf': cache_128_5.miss_rate
    }

    result_128_hit_miss_rate = {
        'gcc': cache_128_1.hit_miss_rate,
        'gzip': cache_128_2.hit_miss_rate,
        'mcf': cache_128_3.hit_miss_rate,
        'swim': cache_128_4.hit_miss_rate,
        'twolf': cache_128_5.hit_miss_rate
    }

    df_B_HitRate['128kB'] = df_B_HitRate.index.map(result_128_hit_rate)
    df_B_MissRate['128kB'] = df_B_MissRate.index.map(result_128_miss_rate)
    df_B_HitMissRate['128kB'] = df_B_HitMissRate.index.map(result_128_hit_miss_rate)

    #for 256kB Cache:
    cache_256_1=Cache(cacheSize=256, accesses='traces/gcc.trace', blockSize=4, wayCount=4)
    cache_256_2=Cache(cacheSize=256, accesses='traces/gzip.trace', blockSize=4, wayCount=4)
    cache_256_3=Cache(cacheSize=256, accesses='traces/mcf.trace', blockSize=4, wayCount=4)
    cache_256_4=Cache(cacheSize=256, accesses='traces/swim.trace', blockSize=4, wayCount=4)
    cache_256_5=Cache(cacheSize=256, accesses='traces/twolf.trace', blockSize=4, wayCount=4)

    result_256_hit_rate = {
        'gcc': cache_256_1.hit_rate,
        'gzip': cache_256_2.hit_rate,
        'mcf': cache_256_3.hit_rate,
        'swim': cache_256_4.hit_rate,
        'twolf': cache_256_5.hit_rate
    }

    result_256_miss_rate = {
        'gcc': cache_256_1.miss_rate,
        'gzip': cache_256_2.miss_rate,
        'mcf': cache_256_3.miss_rate,
        'swim': cache_256_4.miss_rate,
        'twolf': cache_256_5.miss_rate
    }

    result_256_hit_miss_rate = {
        'gcc': cache_256_1.hit_miss_rate,
        'gzip': cache_256_2.hit_miss_rate,
        'mcf': cache_256_3.hit_miss_rate,
        'swim': cache_256_4.hit_miss_rate,
        'twolf': cache_256_5.hit_miss_rate
    }

    df_B_HitRate['256kB'] = df_B_HitRate.index.map(result_256_hit_rate)
    df_B_MissRate['256kB'] = df_B_MissRate.index.map(result_256_miss_rate)
    df_B_HitMissRate['256kB'] = df_B_HitMissRate.index.map(result_256_hit_miss_rate)

    #for 512kB Cache:
    cache_512_1=Cache(cacheSize=512, accesses='traces/gcc.trace', blockSize=4, wayCount=4)
    cache_512_2=Cache(cacheSize=512, accesses='traces/gzip.trace', blockSize=4, wayCount=4)
    cache_512_3=Cache(cacheSize=512, accesses='traces/mcf.trace', blockSize=4, wayCount=4)
    cache_512_4=Cache(cacheSize=512, accesses='traces/swim.trace', blockSize=4, wayCount=4)
    cache_512_5=Cache(cacheSize=512, accesses='traces/twolf.trace', blockSize=4, wayCount=4)

    result_512_hit_rate = {
        'gcc': cache_512_1.hit_rate,
        'gzip': cache_512_2.hit_rate,
        'mcf': cache_512_3.hit_rate,
        'swim': cache_512_4.hit_rate,
        'twolf': cache_512_5.hit_rate
    }

    result_512_miss_rate = {
        'gcc': cache_512_1.miss_rate,
        'gzip': cache_512_2.miss_rate,
        'mcf': cache_512_3.miss_rate,
        'swim': cache_512_4.miss_rate,
        'twolf': cache_512_5.miss_rate
    }

    result_512_hit_miss_rate = {
        'gcc': cache_512_1.hit_miss_rate,
        'gzip': cache_512_2.hit_miss_rate,
        'mcf': cache_512_3.hit_miss_rate,
        'swim': cache_512_4.hit_miss_rate,
        'twolf': cache_512_5.hit_miss_rate
    }

    df_B_HitRate['512kB'] = df_B_HitRate.index.map(result_512_hit_rate)
    df_B_MissRate['512kB'] = df_B_MissRate.index.map(result_512_miss_rate)
    df_B_HitMissRate['512kB'] = df_B_HitMissRate.index.map(result_512_hit_miss_rate)

    #for 1024kB Cache:
    cache_1024_1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=4, wayCount=4)
    cache_1024_2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=4, wayCount=4)
    cache_1024_3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=4, wayCount=4)
    cache_1024_4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=4, wayCount=4)
    cache_1024_5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=4, wayCount=4)

    result_1024_hit_rate = {
        'gcc': cache_1024_1.hit_rate,
        'gzip': cache_1024_2.hit_rate,
        'mcf': cache_1024_3.hit_rate,
        'swim': cache_1024_4.hit_rate,
        'twolf': cache_1024_5.hit_rate
    }

    result_1024_miss_rate = {
        'gcc': cache_1024_1.miss_rate,
        'gzip': cache_1024_2.miss_rate,
        'mcf': cache_1024_3.miss_rate,
        'swim': cache_1024_4.miss_rate,
        'twolf': cache_1024_5.miss_rate
    }

    result_1024_hit_miss_rate = {
        'gcc': cache_1024_1.hit_miss_rate,
        'gzip': cache_1024_2.hit_miss_rate,
        'mcf': cache_1024_3.hit_miss_rate,
        'swim': cache_1024_4.hit_miss_rate,
        'twolf': cache_1024_5.hit_miss_rate
    }

    df_B_HitRate['1024kB'] = df_B_HitRate.index.map(result_1024_hit_rate)
    df_B_MissRate['1024kB'] = df_B_MissRate.index.map(result_1024_miss_rate)
    df_B_HitMissRate['1024kB'] = df_B_HitMissRate.index.map(result_1024_hit_miss_rate)

    #for 2048kB Cache:
    cache_2048_1=Cache(cacheSize=2048, accesses='traces/gcc.trace', blockSize=4, wayCount=4)
    cache_2048_2=Cache(cacheSize=2048, accesses='traces/gzip.trace', blockSize=4, wayCount=4)
    cache_2048_3=Cache(cacheSize=2048, accesses='traces/mcf.trace', blockSize=4, wayCount=4)
    cache_2048_4=Cache(cacheSize=2048, accesses='traces/swim.trace', blockSize=4, wayCount=4)
    cache_2048_5=Cache(cacheSize=2048, accesses='traces/twolf.trace', blockSize=4, wayCount=4)

    result_2048_hit_rate = {
        'gcc': cache_2048_1.hit_rate,
        'gzip': cache_2048_2.hit_rate,
        'mcf': cache_2048_3.hit_rate,
        'swim': cache_2048_4.hit_rate,
        'twolf': cache_2048_5.hit_rate
    }

    result_2048_miss_rate = {
        'gcc': cache_2048_1.miss_rate,
        'gzip': cache_2048_2.miss_rate,
        'mcf': cache_2048_3.miss_rate,
        'swim': cache_2048_4.miss_rate,
        'twolf': cache_2048_5.miss_rate
    }

    result_2048_hit_miss_rate = {
        'gcc': cache_2048_1.hit_miss_rate,
        'gzip': cache_2048_2.hit_miss_rate,
        'mcf': cache_2048_3.hit_miss_rate,
        'swim': cache_2048_4.hit_miss_rate,
        'twolf': cache_2048_5.hit_miss_rate
    }

    df_B_HitRate['2048kB'] = df_B_HitRate.index.map(result_2048_hit_rate)
    df_B_MissRate['2048kB'] = df_B_MissRate.index.map(result_2048_miss_rate)
    df_B_HitMissRate['2048kB'] = df_B_HitMissRate.index.map(result_2048_hit_miss_rate)

    #for 4096kB Cache:
    cache_4096_1=Cache(cacheSize=4096, accesses='traces/gcc.trace', blockSize=4, wayCount=4)
    cache_4096_2=Cache(cacheSize=4096, accesses='traces/gzip.trace', blockSize=4, wayCount=4)
    cache_4096_3=Cache(cacheSize=4096, accesses='traces/mcf.trace', blockSize=4, wayCount=4)
    cache_4096_4=Cache(cacheSize=4096, accesses='traces/swim.trace', blockSize=4, wayCount=4)
    cache_4096_5=Cache(cacheSize=4096, accesses='traces/twolf.trace', blockSize=4, wayCount=4)

    result_4096_hit_rate = {
        'gcc': cache_4096_1.hit_rate,
        'gzip': cache_4096_2.hit_rate,
        'mcf': cache_4096_3.hit_rate,
        'swim': cache_4096_4.hit_rate,
        'twolf': cache_4096_5.hit_rate
    }

    result_4096_miss_rate = {
        'gcc': cache_4096_1.miss_rate,
        'gzip': cache_4096_2.miss_rate,
        'mcf': cache_4096_3.miss_rate,
        'swim': cache_4096_4.miss_rate,
        'twolf': cache_4096_5.miss_rate
    }

    result_4096_hit_miss_rate = {
        'gcc': cache_4096_1.hit_miss_rate,
        'gzip': cache_4096_2.hit_miss_rate,
        'mcf': cache_4096_3.hit_miss_rate,
        'swim': cache_4096_4.hit_miss_rate,
        'twolf': cache_4096_5.hit_miss_rate
    }

    df_B_HitRate['4096kB'] = df_B_HitRate.index.map(result_4096_hit_rate)
    df_B_MissRate['4096kB'] = df_B_MissRate.index.map(result_4096_miss_rate)
    df_B_HitMissRate['4096kB'] = df_B_HitMissRate.index.map(result_4096_hit_miss_rate)

    #Printing the dataframes
    print("Answer to Question B:")
    print("These are the hit rate, miss rate and Hit/Miss Ratio for the given Cache when the cache size is varied.\n")
    print("Hit Rate:")
    print(tabulate(df_B_HitRate, headers='keys', tablefmt='grid'))
    print("\n")
    print("Miss Rate:")
    print(tabulate(df_B_MissRate, headers='keys', tablefmt='grid'))
    print("\n")
    print("Hit/Miss Ratio:")
    print(tabulate(df_B_HitMissRate, headers='keys', tablefmt='grid'))
    print("\n")

    # Plotting Miss Rate Graph
    plt.figure(figsize=(12, 8))
    for index in df_B_MissRate.index:
        plt.plot(df_B_MissRate.columns, df_B_MissRate.loc[index], marker='o', label=f'{index} Miss Rate')

    plt.title('Cache Miss Rate vs Cache Size')
    plt.xlabel('Cache Size')
    plt.ylabel('Miss Rate')
    plt.legend(title='Benchmark')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plotting Hit Rate Graph
    plt.figure(figsize=(12, 8))
    for index in df_B_HitRate.index:
        plt.plot(df_B_HitRate.columns, df_B_HitRate.loc[index], marker='o', label=f'{index} Hit Rate')

    plt.title('Cache Hit Rate vs Cache Size')
    plt.xlabel('Cache Size')
    plt.ylabel('Hit Rate')
    plt.legend(title='Benchmark')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


###############################################################################

############################## Question Part (C) ##############################

df_C_HitRate = pd.DataFrame(index=['gcc', 'gzip', 'mcf', 'swim', 'twolf'])
df_C_MissRate = pd.DataFrame(index=['gcc', 'gzip', 'mcf', 'swim', 'twolf'])
df_C_HitMissRate = pd.DataFrame(index=['gcc', 'gzip', 'mcf', 'swim', 'twolf'])

def QuestionC():
    #for 1B Block Size
    cache_blockSize1_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=1, wayCount=4)
    cache_blockSize1_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=1, wayCount=4)
    cache_blockSize1_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=1, wayCount=4)
    cache_blockSize1_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=1, wayCount=4)
    cache_blockSize1_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=1, wayCount=4)

    result_1_hit_rate = {
        'gcc': cache_blockSize1_trace1.hit_rate,
        'gzip': cache_blockSize1_trace2.hit_rate,
        'mcf': cache_blockSize1_trace3.hit_rate,
        'swim': cache_blockSize1_trace4.hit_rate,
        'twolf': cache_blockSize1_trace5.hit_rate
    }

    result_1_miss_rate = {
        'gcc': cache_blockSize1_trace1.miss_rate,
        'gzip': cache_blockSize1_trace2.miss_rate,
        'mcf': cache_blockSize1_trace3.miss_rate,
        'swim': cache_blockSize1_trace4.miss_rate,
        'twolf': cache_blockSize1_trace5.miss_rate
    }

    result_1_hit_miss_rate = {
        'gcc': cache_blockSize1_trace1.hit_miss_rate,
        'gzip': cache_blockSize1_trace2.hit_miss_rate,
        'mcf': cache_blockSize1_trace3.hit_miss_rate,
        'swim': cache_blockSize1_trace4.hit_miss_rate,
        'twolf': cache_blockSize1_trace5.hit_miss_rate
    }

    df_C_HitRate['1B'] = df_C_HitRate.index.map(result_1_hit_rate)
    df_C_MissRate['1B'] = df_C_MissRate.index.map(result_1_miss_rate)
    df_C_HitMissRate['1B'] = df_C_HitMissRate.index.map(result_1_hit_miss_rate)

    #for 2B Block Size
    cache_blockSize2_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=2, wayCount=4)
    cache_blockSize2_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=2, wayCount=4)
    cache_blockSize2_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=2, wayCount=4)
    cache_blockSize2_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=2, wayCount=4)
    cache_blockSize2_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=2, wayCount=4)

    result_2_hit_rate = {
        'gcc': cache_blockSize2_trace1.hit_rate,
        'gzip': cache_blockSize2_trace2.hit_rate,
        'mcf': cache_blockSize2_trace3.hit_rate,
        'swim': cache_blockSize2_trace4.hit_rate,
        'twolf': cache_blockSize2_trace5.hit_rate
    }

    result_2_miss_rate = {
        'gcc': cache_blockSize2_trace1.miss_rate,
        'gzip': cache_blockSize2_trace2.miss_rate,
        'mcf': cache_blockSize2_trace3.miss_rate,
        'swim': cache_blockSize2_trace4.miss_rate,
        'twolf': cache_blockSize2_trace5.miss_rate
    }

    result_2_hit_miss_rate = {
        'gcc': cache_blockSize2_trace1.hit_miss_rate,
        'gzip': cache_blockSize2_trace2.hit_miss_rate,
        'mcf': cache_blockSize2_trace3.hit_miss_rate,
        'swim': cache_blockSize2_trace4.hit_miss_rate,
        'twolf': cache_blockSize2_trace5.hit_miss_rate
    }

    df_C_HitRate['2B'] = df_C_HitRate.index.map(result_2_hit_rate)
    df_C_MissRate['2B'] = df_C_MissRate.index.map(result_2_miss_rate)
    df_C_HitMissRate['2B'] = df_C_HitMissRate.index.map(result_2_hit_miss_rate)

    #for 4B Block Size
    cache_blockSize4_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=4, wayCount=4)
    cache_blockSize4_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=4, wayCount=4)
    cache_blockSize4_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=4, wayCount=4)
    cache_blockSize4_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=4, wayCount=4)
    cache_blockSize4_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=4, wayCount=4)

    result_4_hit_rate = {
        'gcc': cache_blockSize4_trace1.hit_rate,
        'gzip': cache_blockSize4_trace2.hit_rate,
        'mcf': cache_blockSize4_trace3.hit_rate,
        'swim': cache_blockSize4_trace4.hit_rate,
        'twolf': cache_blockSize4_trace5.hit_rate
    }

    result_4_miss_rate = {
        'gcc': cache_blockSize4_trace1.miss_rate,
        'gzip': cache_blockSize4_trace2.miss_rate,
        'mcf': cache_blockSize4_trace3.miss_rate,
        'swim': cache_blockSize4_trace4.miss_rate,
        'twolf': cache_blockSize4_trace5.miss_rate
    }

    result_4_hit_miss_rate = {
        'gcc': cache_blockSize4_trace1.hit_miss_rate,
        'gzip': cache_blockSize4_trace2.hit_miss_rate,
        'mcf': cache_blockSize4_trace3.hit_miss_rate,
        'swim': cache_blockSize4_trace4.hit_miss_rate,
        'twolf': cache_blockSize4_trace5.hit_miss_rate
    }

    df_C_HitRate['4B'] = df_C_HitRate.index.map(result_4_hit_rate)
    df_C_MissRate['4B'] = df_C_MissRate.index.map(result_4_miss_rate)
    df_C_HitMissRate['4B'] = df_C_HitMissRate.index.map(result_4_hit_miss_rate)

    #for 8B Block Size
    cache_blockSize8_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=8, wayCount=4)
    cache_blockSize8_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=8, wayCount=4)
    cache_blockSize8_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=8, wayCount=4)
    cache_blockSize8_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=8, wayCount=4)
    cache_blockSize8_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=8, wayCount=4)

    result_8_hit_rate = {
        'gcc': cache_blockSize8_trace1.hit_rate,
        'gzip': cache_blockSize8_trace2.hit_rate,
        'mcf': cache_blockSize8_trace3.hit_rate,
        'swim': cache_blockSize8_trace4.hit_rate,
        'twolf': cache_blockSize8_trace5.hit_rate
    }

    result_8_miss_rate = {
        'gcc': cache_blockSize8_trace1.miss_rate,
        'gzip': cache_blockSize8_trace2.miss_rate,
        'mcf': cache_blockSize8_trace3.miss_rate,
        'swim': cache_blockSize8_trace4.miss_rate,
        'twolf': cache_blockSize8_trace5.miss_rate
    }

    result_8_hit_miss_rate = {
        'gcc': cache_blockSize8_trace1.hit_miss_rate,
        'gzip': cache_blockSize8_trace2.hit_miss_rate,
        'mcf': cache_blockSize8_trace3.hit_miss_rate,
        'swim': cache_blockSize8_trace4.hit_miss_rate,
        'twolf': cache_blockSize8_trace5.hit_miss_rate
    }

    df_C_HitRate['8B'] = df_C_HitRate.index.map(result_8_hit_rate)
    df_C_MissRate['8B'] = df_C_MissRate.index.map(result_8_miss_rate)
    df_C_HitMissRate['8B'] = df_C_HitMissRate.index.map(result_8_hit_miss_rate)

    #for 16B Block Size
    cache_blockSize16_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=16, wayCount=4)
    cache_blockSize16_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=16, wayCount=4)
    cache_blockSize16_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=16, wayCount=4)
    cache_blockSize16_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=16, wayCount=4)
    cache_blockSize16_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=16, wayCount=4)

    result_16_hit_rate = {
        'gcc': cache_blockSize16_trace1.hit_rate,
        'gzip': cache_blockSize16_trace2.hit_rate,
        'mcf': cache_blockSize16_trace3.hit_rate,
        'swim': cache_blockSize16_trace4.hit_rate,
        'twolf': cache_blockSize16_trace5.hit_rate
    }

    result_16_miss_rate = {
        'gcc': cache_blockSize16_trace1.miss_rate,
        'gzip': cache_blockSize16_trace2.miss_rate,
        'mcf': cache_blockSize16_trace3.miss_rate,
        'swim': cache_blockSize16_trace4.miss_rate,
        'twolf': cache_blockSize16_trace5.miss_rate
    }

    result_16_hit_miss_rate = {
        'gcc': cache_blockSize16_trace1.hit_miss_rate,
        'gzip': cache_blockSize16_trace2.hit_miss_rate,
        'mcf': cache_blockSize16_trace3.hit_miss_rate,
        'swim': cache_blockSize16_trace4.hit_miss_rate,
        'twolf': cache_blockSize16_trace5.hit_miss_rate
    }

    df_C_HitRate['16B'] = df_C_HitRate.index.map(result_16_hit_rate)
    df_C_MissRate['16B'] = df_C_MissRate.index.map(result_16_miss_rate)
    df_C_HitMissRate['16B'] = df_C_HitMissRate.index.map(result_16_hit_miss_rate)

    #for 32B Block Size
    cache_blockSize32_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=32, wayCount=4)
    cache_blockSize32_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=32, wayCount=4)
    cache_blockSize32_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=32, wayCount=4)
    cache_blockSize32_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=32, wayCount=4)
    cache_blockSize32_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=32, wayCount=4)

    result_32_hit_rate = {
        'gcc': cache_blockSize32_trace1.hit_rate,
        'gzip': cache_blockSize32_trace2.hit_rate,
        'mcf': cache_blockSize32_trace3.hit_rate,
        'swim': cache_blockSize32_trace4.hit_rate,
        'twolf': cache_blockSize32_trace5.hit_rate
    }

    result_32_miss_rate = {
        'gcc': cache_blockSize32_trace1.miss_rate,
        'gzip': cache_blockSize32_trace2.miss_rate,
        'mcf': cache_blockSize32_trace3.miss_rate,
        'swim': cache_blockSize32_trace4.miss_rate,
        'twolf': cache_blockSize32_trace5.miss_rate
    }

    result_32_hit_miss_rate = {
        'gcc': cache_blockSize32_trace1.hit_miss_rate,
        'gzip': cache_blockSize32_trace2.hit_miss_rate,
        'mcf': cache_blockSize32_trace3.hit_miss_rate,
        'swim': cache_blockSize32_trace4.hit_miss_rate,
        'twolf': cache_blockSize32_trace5.hit_miss_rate
    }

    df_C_HitRate['32B'] = df_C_HitRate.index.map(result_32_hit_rate)
    df_C_MissRate['32B'] = df_C_MissRate.index.map(result_32_miss_rate)
    df_C_HitMissRate['32B'] = df_C_HitMissRate.index.map(result_32_hit_miss_rate)

    #for 64B Block Size
    cache_blockSize64_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=64, wayCount=4)
    cache_blockSize64_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=64, wayCount=4)
    cache_blockSize64_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=64, wayCount=4)
    cache_blockSize64_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=64, wayCount=4)
    cache_blockSize64_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=64, wayCount=4)

    result_64_hit_rate = {
        'gcc': cache_blockSize64_trace1.hit_rate,
        'gzip': cache_blockSize64_trace2.hit_rate,
        'mcf': cache_blockSize64_trace3.hit_rate,
        'swim': cache_blockSize64_trace4.hit_rate,
        'twolf': cache_blockSize64_trace5.hit_rate
    }

    result_64_miss_rate = {
        'gcc': cache_blockSize64_trace1.miss_rate,
        'gzip': cache_blockSize64_trace2.miss_rate,
        'mcf': cache_blockSize64_trace3.miss_rate,
        'swim': cache_blockSize64_trace4.miss_rate,
        'twolf': cache_blockSize64_trace5.miss_rate
    }

    result_64_hit_miss_rate = {
        'gcc': cache_blockSize64_trace1.hit_miss_rate,
        'gzip': cache_blockSize64_trace2.hit_miss_rate,
        'mcf': cache_blockSize64_trace3.hit_miss_rate,
        'swim': cache_blockSize64_trace4.hit_miss_rate,
        'twolf': cache_blockSize64_trace5.hit_miss_rate
    }

    df_C_HitRate['64B'] = df_C_HitRate.index.map(result_64_hit_rate)
    df_C_MissRate['64B'] = df_C_MissRate.index.map(result_64_miss_rate)
    df_C_HitMissRate['64B'] = df_C_HitMissRate.index.map(result_64_hit_miss_rate)

    #for 128B Block Size
    cache_blockSize128_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=128, wayCount=4)
    cache_blockSize128_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=128, wayCount=4)
    cache_blockSize128_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=128, wayCount=4)
    cache_blockSize128_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=128, wayCount=4)
    cache_blockSize128_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=128, wayCount=4)

    result_128_hit_rate = {
        'gcc': cache_blockSize128_trace1.hit_rate,
        'gzip': cache_blockSize128_trace2.hit_rate,
        'mcf': cache_blockSize128_trace3.hit_rate,
        'swim': cache_blockSize128_trace4.hit_rate,
        'twolf': cache_blockSize128_trace5.hit_rate
    }

    result_128_miss_rate = {
        'gcc': cache_blockSize128_trace1.miss_rate,
        'gzip': cache_blockSize128_trace2.miss_rate,
        'mcf': cache_blockSize128_trace3.miss_rate,
        'swim': cache_blockSize128_trace4.miss_rate,
        'twolf': cache_blockSize128_trace5.miss_rate
    }

    result_128_hit_miss_rate = {
        'gcc': cache_blockSize128_trace1.hit_miss_rate,
        'gzip': cache_blockSize128_trace2.hit_miss_rate,
        'mcf': cache_blockSize128_trace3.hit_miss_rate,
        'swim': cache_blockSize128_trace4.hit_miss_rate,
        'twolf': cache_blockSize128_trace5.hit_miss_rate
    }

    df_C_HitRate['128B'] = df_C_HitRate.index.map(result_128_hit_rate)
    df_C_MissRate['128B'] = df_C_MissRate.index.map(result_128_miss_rate)
    df_C_HitMissRate['128B'] = df_C_HitMissRate.index.map(result_128_hit_miss_rate)

    print("Answer to Question C:")
    print("These are the hit rate, miss rate, and Hit/Miss Ratio for the given Cache when the block size is varied.\n")
    print("Hit Rate:")
    print(tabulate(df_C_HitRate, headers='keys', tablefmt='grid'))
    print("\n")
    print("Miss Rate:")
    print(tabulate(df_C_MissRate, headers='keys', tablefmt='grid'))
    print("\n")
    print("Hit/Miss Ratio:")
    print(tabulate(df_C_HitMissRate, headers='keys', tablefmt='grid'))
    print("\n")

    # Plotting Miss Rate Graph
    plt.figure(figsize=(10, 6))
    for row in df_C_MissRate.index:
        plt.plot(df_C_MissRate.columns, df_C_MissRate.loc[row], label=f'{row} Miss Rate')

    plt.title('Cache Miss Rate vs Block Size')
    plt.xlabel('Block Size')
    plt.ylabel('Miss Rate')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plotting Hit Rate Graph
    plt.figure(figsize=(10, 6))
    for row in df_C_HitRate.index:
        plt.plot(df_C_HitRate.columns, df_C_HitRate.loc[row], label=f'{row} Hit Rate')

    plt.title('Cache Hit Rate vs Block Size')
    plt.xlabel('Block Size')
    plt.ylabel('Hit Rate')
    plt.legend()
    plt.grid(True)
    plt.show()



###############################################################################

############################## Question Part (D) ##############################

df_D_HitRate = pd.DataFrame(index=['gcc', 'gzip', 'mcf', 'swim', 'twolf'])
df_D_MissRate = pd.DataFrame(index=['gcc', 'gzip', 'mcf', 'swim', 'twolf'])
df_D_HitMissRate = pd.DataFrame(index=['gcc', 'gzip', 'mcf', 'swim', 'twolf'])

def QuestionD():
    #for 1 way SA
    cache_ways1_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=4, wayCount=1)
    cache_ways1_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=4, wayCount=1)
    cache_ways1_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=4, wayCount=1)
    cache_ways1_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=4, wayCount=1)
    cache_ways1_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=4, wayCount=1)

    result_1_hit_rate = {
        'gcc': cache_ways1_trace1.hit_rate,
        'gzip': cache_ways1_trace2.hit_rate,
        'mcf': cache_ways1_trace3.hit_rate,
        'swim': cache_ways1_trace4.hit_rate,
        'twolf': cache_ways1_trace5.hit_rate
    }

    result_1_miss_rate = {
        'gcc': cache_ways1_trace1.miss_rate,
        'gzip': cache_ways1_trace2.miss_rate,
        'mcf': cache_ways1_trace3.miss_rate,
        'swim': cache_ways1_trace4.miss_rate,
        'twolf': cache_ways1_trace5.miss_rate
    }

    result_1_hit_miss_rate = {
        'gcc': cache_ways1_trace1.hit_miss_rate,
        'gzip': cache_ways1_trace2.hit_miss_rate,
        'mcf': cache_ways1_trace3.hit_miss_rate,
        'swim': cache_ways1_trace4.hit_miss_rate,
        'twolf': cache_ways1_trace5.hit_miss_rate
    }

    df_D_HitRate['1 way'] = df_D_HitRate.index.map(result_1_hit_rate)
    df_D_MissRate['1 way'] = df_D_MissRate.index.map(result_1_miss_rate)
    df_D_HitMissRate['1 way'] = df_D_HitMissRate.index.map(result_1_hit_miss_rate)

    #for 2 way SA
    cache_ways2_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=4, wayCount=2)
    cache_ways2_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=4, wayCount=2)
    cache_ways2_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=4, wayCount=2)
    cache_ways2_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=4, wayCount=2)
    cache_ways2_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=4, wayCount=2)

    result_2_hit_rate = {
        'gcc': cache_ways2_trace1.hit_rate,
        'gzip': cache_ways2_trace2.hit_rate,
        'mcf': cache_ways2_trace3.hit_rate,
        'swim': cache_ways2_trace4.hit_rate,
        'twolf': cache_ways2_trace5.hit_rate
    }

    result_2_miss_rate = {
        'gcc': cache_ways2_trace1.miss_rate,
        'gzip': cache_ways2_trace2.miss_rate,
        'mcf': cache_ways2_trace3.miss_rate,
        'swim': cache_ways2_trace4.miss_rate,
        'twolf': cache_ways2_trace5.miss_rate
    }

    result_2_hit_miss_rate = {
        'gcc': cache_ways2_trace1.hit_miss_rate,
        'gzip': cache_ways2_trace2.hit_miss_rate,
        'mcf': cache_ways2_trace3.hit_miss_rate,
        'swim': cache_ways2_trace4.hit_miss_rate,
        'twolf': cache_ways2_trace5.hit_miss_rate
    }

    df_D_HitRate['2 way'] = df_D_HitRate.index.map(result_2_hit_rate)
    df_D_MissRate['2 way'] = df_D_MissRate.index.map(result_2_miss_rate)
    df_D_HitMissRate['2 way'] = df_D_HitMissRate.index.map(result_2_hit_miss_rate)

    #for 4 way SA
    cache_ways4_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=4, wayCount=4)
    cache_ways4_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=4, wayCount=4)
    cache_ways4_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=4, wayCount=4)
    cache_ways4_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=4, wayCount=4)
    cache_ways4_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=4, wayCount=4)

    result_4_hit_rate = {
        'gcc': cache_ways4_trace1.hit_rate,
        'gzip': cache_ways4_trace2.hit_rate,
        'mcf': cache_ways4_trace3.hit_rate,
        'swim': cache_ways4_trace4.hit_rate,
        'twolf': cache_ways4_trace5.hit_rate
    }

    result_4_miss_rate = {
        'gcc': cache_ways4_trace1.miss_rate,
        'gzip': cache_ways4_trace2.miss_rate,
        'mcf': cache_ways4_trace3.miss_rate,
        'swim': cache_ways4_trace4.miss_rate,
        'twolf': cache_ways4_trace5.miss_rate
    }

    result_4_hit_miss_rate = {
        'gcc': cache_ways4_trace1.hit_miss_rate,
        'gzip': cache_ways4_trace2.hit_miss_rate,
        'mcf': cache_ways4_trace3.hit_miss_rate,
        'swim': cache_ways4_trace4.hit_miss_rate,
        'twolf': cache_ways4_trace5.hit_miss_rate
    }

    df_D_HitRate['4 way'] = df_D_HitRate.index.map(result_4_hit_rate)
    df_D_MissRate['4 way'] = df_D_MissRate.index.map(result_4_miss_rate)
    df_D_HitMissRate['4 way'] = df_D_HitMissRate.index.map(result_4_hit_miss_rate)

    #for 8 way SA
    cache_ways8_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=4, wayCount=8)
    cache_ways8_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=4, wayCount=8)
    cache_ways8_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=4, wayCount=8)
    cache_ways8_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=4, wayCount=8)
    cache_ways8_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=4, wayCount=8)

    result_8_hit_rate = {
        'gcc': cache_ways8_trace1.hit_rate,
        'gzip': cache_ways8_trace2.hit_rate,
        'mcf': cache_ways8_trace3.hit_rate,
        'swim': cache_ways8_trace4.hit_rate,
        'twolf': cache_ways8_trace5.hit_rate
    }

    result_8_miss_rate = {
        'gcc': cache_ways8_trace1.miss_rate,
        'gzip': cache_ways8_trace2.miss_rate,
        'mcf': cache_ways8_trace3.miss_rate,
        'swim': cache_ways8_trace4.miss_rate,
        'twolf': cache_ways8_trace5.miss_rate
    }

    result_8_hit_miss_rate = {
        'gcc': cache_ways8_trace1.hit_miss_rate,
        'gzip': cache_ways8_trace2.hit_miss_rate,
        'mcf': cache_ways8_trace3.hit_miss_rate,
        'swim': cache_ways8_trace4.hit_miss_rate,
        'twolf': cache_ways8_trace5.hit_miss_rate
    }

    df_D_HitRate['8 way'] = df_D_HitRate.index.map(result_8_hit_rate)
    df_D_MissRate['8 way'] = df_D_MissRate.index.map(result_8_miss_rate)
    df_D_HitMissRate['8 way'] = df_D_HitMissRate.index.map(result_8_hit_miss_rate)

    #for 16 way SA
    cache_ways16_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=4, wayCount=16)
    cache_ways16_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=4, wayCount=16)
    cache_ways16_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=4, wayCount=16)
    cache_ways16_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=4, wayCount=16)
    cache_ways16_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=4, wayCount=16)

    result_16_hit_rate = {
        'gcc': cache_ways16_trace1.hit_rate,
        'gzip': cache_ways16_trace2.hit_rate,
        'mcf': cache_ways16_trace3.hit_rate,
        'swim': cache_ways16_trace4.hit_rate,
        'twolf': cache_ways16_trace5.hit_rate
    }

    result_16_miss_rate = {
        'gcc': cache_ways16_trace1.miss_rate,
        'gzip': cache_ways16_trace2.miss_rate,
        'mcf': cache_ways16_trace3.miss_rate,
        'swim': cache_ways16_trace4.miss_rate,
        'twolf': cache_ways16_trace5.miss_rate
    }

    result_16_hit_miss_rate = {
        'gcc': cache_ways16_trace1.hit_miss_rate,
        'gzip': cache_ways16_trace2.hit_miss_rate,
        'mcf': cache_ways16_trace3.hit_miss_rate,
        'swim': cache_ways16_trace4.hit_miss_rate,
        'twolf': cache_ways16_trace5.hit_miss_rate
    }

    df_D_HitRate['16 way'] = df_D_HitRate.index.map(result_16_hit_rate)
    df_D_MissRate['16 way'] = df_D_MissRate.index.map(result_16_miss_rate)
    df_D_HitMissRate['16 way'] = df_D_HitMissRate.index.map(result_16_hit_miss_rate)

    #for 32 way SA
    cache_ways32_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=4, wayCount=32)
    cache_ways32_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=4, wayCount=32)
    cache_ways32_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=4, wayCount=32)
    cache_ways32_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=4, wayCount=32)
    cache_ways32_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=4, wayCount=32)

    result_32_hit_rate = {
        'gcc': cache_ways32_trace1.hit_rate,
        'gzip': cache_ways32_trace2.hit_rate,
        'mcf': cache_ways32_trace3.hit_rate,
        'swim': cache_ways32_trace4.hit_rate,
        'twolf': cache_ways32_trace5.hit_rate
    }

    result_32_miss_rate = {
        'gcc': cache_ways32_trace1.miss_rate,
        'gzip': cache_ways32_trace2.miss_rate,
        'mcf': cache_ways32_trace3.miss_rate,
        'swim': cache_ways32_trace4.miss_rate,
        'twolf': cache_ways32_trace5.miss_rate
    }

    result_32_hit_miss_rate = {
        'gcc': cache_ways32_trace1.hit_miss_rate,
        'gzip': cache_ways32_trace2.hit_miss_rate,
        'mcf': cache_ways32_trace3.hit_miss_rate,
        'swim': cache_ways32_trace4.hit_miss_rate,
        'twolf': cache_ways32_trace5.hit_miss_rate
    }

    df_D_HitRate['32 way'] = df_D_HitRate.index.map(result_32_hit_rate)
    df_D_MissRate['32 way'] = df_D_MissRate.index.map(result_32_miss_rate)
    df_D_HitMissRate['32 way'] = df_D_HitMissRate.index.map(result_32_hit_miss_rate)

    #for 64 way SA
    cache_ways64_trace1=Cache(cacheSize=1024, accesses='traces/gcc.trace', blockSize=4, wayCount=64)
    cache_ways64_trace2=Cache(cacheSize=1024, accesses='traces/gzip.trace', blockSize=4, wayCount=64)
    cache_ways64_trace3=Cache(cacheSize=1024, accesses='traces/mcf.trace', blockSize=4, wayCount=64)
    cache_ways64_trace4=Cache(cacheSize=1024, accesses='traces/swim.trace', blockSize=4, wayCount=64)
    cache_ways64_trace5=Cache(cacheSize=1024, accesses='traces/twolf.trace', blockSize=4, wayCount=64)

    result_64_hit_rate = {
        'gcc': cache_ways64_trace1.hit_rate,
        'gzip': cache_ways64_trace2.hit_rate,
        'mcf': cache_ways64_trace3.hit_rate,
        'swim': cache_ways64_trace4.hit_rate,
        'twolf': cache_ways64_trace5.hit_rate
    }

    result_64_miss_rate = {
        'gcc': cache_ways64_trace1.miss_rate,
        'gzip': cache_ways64_trace2.miss_rate,
        'mcf': cache_ways64_trace3.miss_rate,
        'swim': cache_ways64_trace4.miss_rate,
        'twolf': cache_ways64_trace5.miss_rate
    }

    result_64_hit_miss_rate = {
        'gcc': cache_ways64_trace1.hit_miss_rate,
        'gzip': cache_ways64_trace2.hit_miss_rate,
        'mcf': cache_ways64_trace3.hit_miss_rate,
        'swim': cache_ways64_trace4.hit_miss_rate,
        'twolf': cache_ways64_trace5.hit_miss_rate
    }

    df_D_HitRate['64 way'] = df_D_HitRate.index.map(result_64_hit_rate)
    df_D_MissRate['64 way'] = df_D_MissRate.index.map(result_64_miss_rate)
    df_D_HitMissRate['64 way'] = df_D_HitMissRate.index.map(result_64_hit_miss_rate)

    print("Answer to Question D:")
    print("These are the hit rate, miss rate and Hit/Miss Ratio for the given Cache when the no. of cache ways is varied.\n")
    print("Hit Rate:")
    print(tabulate(df_D_HitRate, headers='keys', tablefmt='grid'))
    print("\n")
    print("Miss Rate:")
    print(tabulate(df_D_MissRate, headers='keys', tablefmt='grid'))
    print("\n")
    print("Hit/Miss Ratio:")
    print(tabulate(df_D_HitMissRate, headers='keys', tablefmt='grid'))
    print("\n")

    # Plotting Miss Rate Graph
    plt.figure(figsize=(10, 6))
    for row in df_D_MissRate.index:
        plt.plot(df_D_MissRate.columns, df_D_MissRate.loc[row], label=f'{row} Miss Rate')

    plt.title('Cache Miss Rate vs No. of Cache Ways')
    plt.xlabel('No. of Cache Ways')
    plt.ylabel('Miss Rate')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plotting Hit Rate Graph
    plt.figure(figsize=(10, 6))
    for row in df_D_HitRate.index:
        plt.plot(df_D_HitRate.columns, df_D_HitRate.loc[row], label=f'{row} Hit Rate')

    plt.title('Cache Hit Rate vs No. of Cache Ways')
    plt.xlabel('No. of Cache Ways')
    plt.ylabel('Hit Rate')
    plt.legend()
    plt.grid(True)
    plt.show()


###############################################################################
###############################################################################

print("\n-------------------------------------------------------------------")
print("------------------------- Cache Simulator -------------------------")
print("-------------------------------------------------------------------\n")

while True:
    prompt = '''Enter the integer to view the corresponding answer of the question: 
    1) Question A [Hit rate, Miss rate, Hit/Miss ratio for the given cache]
    2) Question B [Hit rate, Miss rate, Hit/Miss ratio for the given cache when the cache size is varied]
    3) Question C [Hit rate, Miss rate, Hit/Miss ratio for the given cache when the block size is varied]
    4) Question D [Hit rate, Miss rate, Hit/Miss ratio for the given cache when the number of cache ways is varied]
    -1) Exit'''

    print(prompt)
    a = int(input("Enter the integer: "))
    print("\n")

    if a == 1:
        QuestionA()
    elif a == 2:
        QuestionB()
    elif a == 3:
        QuestionC()
    elif a == 4:
        QuestionD()
    elif a == -1:
        break
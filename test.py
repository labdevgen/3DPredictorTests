import sys
import os
import datetime
from memory_profiler import memory_usage

source_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),
                           "3Dpredictor/source")
print (source_path)
sys.path.append(source_path)
from shared import intersect_with_interval, \
    intersect_with_interval_v2, intersect_with_interval_v3, \
    intersect_with_interval_v4, Interval
from intervaltree import IntervalTree
import random
random.seed()
import pandas as pd
import  numpy as np

def compare_results(res_v1,res_intTree):
    if len(res_v1) == len(res_intTree) == 0:
        return True
    if len(res_v1) != len(res_intTree):
        return False
    return  np.array_equal(sorted(res_v1.ids.values),
                                sorted(res_intTree))
def create_intervals():
    # Create some interavals
    N_intervals = 50000
    global  minLen
    minLen = 100
    global  maxLen
    maxLen = 1000
    global maxPos
    maxPos = 100000000

    starts = []
    ends = []
    indexes = []
    tree = IntervalTree()

    start = 0
    l = 0
    for i in range(0,N_intervals):
        start = random.randint(0,maxPos)
        #start = start + l + 2
        l = random.randint(minLen,maxLen)
        tree[start:start+l+1] = i
        starts.append(start)
        ends.append(start+l)
        indexes.append(i)

    tree[2000:3001] = N_intervals
    tree[2500:2601] = N_intervals+1
    starts += [2000,2500]
    ends += [3000,2600]
    indexes += [N_intervals,N_intervals+1]

    df = pd.DataFrame({"start":starts,"end":ends,"ids":indexes})
    df2 = pd.concat([df[["start","ids"]].rename(columns={"start":"coordinate"}),
                     df[["end","ids"]].rename(columns={"end":"coordinate"})],
                    axis="rows")
    df2["type"] = ["start"]*len(df) + ["end"]*len(df)
    df2.sort_values(by="coordinate", inplace=True)
    return  tree, df, df2

def compare_intervalfuncs(tree, df, df2, df3):
    data1 = {"chr1":df}
    data2 = {"chr1":df2}
    data3 = {"chr1":df3}

    count_match_v1 = 0
    count_match_v2 = 0
    count_match_v3 = 0
    count_match_v4 = 0
    N_tests = 100
    for i in range(0,N_tests):
        start = random.randint(0,maxPos)
        l = random.randint(minLen,maxLen*5)
        # start = 2200
        # l = 2550 - 2200
        interval = Interval("chr1",start,start+l)
        res_v1 = intersect_with_interval(data1,interval)
        res_v2 = intersect_with_interval_v2(data2, interval)
        if len(res_v2) > 0:
            ids = np.unique(res_v2.ids.values)
            res_v2 = df.loc[ids]
            #print (res_v2)
            #break
        res_v3 = intersect_with_interval_v3(data1,interval)
        res_v4 = intersect_with_interval_v4(data3,interval)
        res_intTree = np.array([ q.data for q in tree[start:start+l+1] ])
        match_v1 = compare_results(res_v1,res_intTree)
        match_v2 = compare_results(res_v2,res_intTree)
        match_v3 = compare_results(res_v3,res_intTree)
        match_v4 = compare_results(res_v4,res_intTree)
        count_match_v1 += match_v1
        count_match_v2 += match_v2
        count_match_v3 += match_v3
        count_match_v4 += match_v4
        if not match_v3:
            print("---------------")
            print (interval)
            print (res_v3)
            print (res_intTree)
    print(count_match_v1, " of ", N_tests)
    print(count_match_v2, " of ", N_tests)
    print(count_match_v3, " of ", N_tests)
    print(count_match_v4, " of ", N_tests)

def run_timing(func,data,N):
    now = datetime.datetime.now()
    data_dict = {"chr1": data}
    for i in range(0,N):
        start = random.randint(0,maxPos)
        l = random.randint(minLen,maxLen*5)
        interval = Interval("chr1",start,start+l)
        res = func(data_dict,interval)
    now2 = datetime.datetime.now()
    print (str(func.__name__)," : ",now2-now)

def df2intervals(df):
    result=df.copy()
    newindex = pd.IntervalIndex.from_tuples(
                df.apply(lambda x: (x.start,
                                    x.end), axis="columns"),
                                          closed="both")
    result = result.set_index(newindex)
    return result


tree, df, df2 = create_intervals()
df3 = df2intervals(df)
df3.index.overlaps(pd.Interval(0,1000))
#compare_intervalfuncs(tree,df,df2,df3)
N=100

for func,data in zip([intersect_with_interval,
                        intersect_with_interval_v2,
                        intersect_with_interval_v3,
                        intersect_with_interval_v4],
                        [df,df2,df,df3]):
    mem = memory_usage((run_timing, (func,data,N)),interval=.5)
    print ("Max memory: ",max(mem))
    print("Memory log: ",mem)
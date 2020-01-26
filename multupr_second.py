import sys, os
import time
from multiprocessing import Pool
source_path = os.path.join(os.path.dirname(os.path.abspath(os.path.abspath(__file__))),
                           "3Dpredictor/source")
sys.path.append(source_path)
from DataGenerator import get_split_array_indexes

def initializer(CWorker_object):
    global mpCWorker_object
    mpCWorker_object = CWorker_object
    print ("0",id(mpCWorker_object),
           id(mpCWorker_object.large_data),
           id(mpCWorker_object.large_data[0]))
    return

def work(args):
    #st, en, mpCWorker_object = args
    st, en, ind  = args
    time.sleep(ind)
    print("---------Calculating res")
    print("Before: ",mpCWorker_object.large_data[0])
    print (ind,id(mpCWorker_object),
           id(mpCWorker_object.large_data),
           id(mpCWorker_object.large_data[0]))
    res = sum(mpCWorker_object.large_data[max(0,st-3):en])
    #mpCWorker_object.large_data += 10
    #mpCWorker_object.large_data = [100,2,3]
    print("After: ",mpCWorker_object.large_data[0])
    print (ind, id(mpCWorker_object),
           id(mpCWorker_object.large_data),
           id(mpCWorker_object.large_data[0]))
    res = 1
    time.sleep(3)
    return res

class CWorker():
    def __init__(self,large_data):
        self.large_data = large_data
    def start_work(self):
        n_cpus = 3
        print ("init pool")
        print("0",id(self),
              id(self.large_data),
              id(self.large_data[0]))
        #initializer(self)
        pool = Pool(processes=n_cpus, initializer=initializer, initargs=(self,))
        start_points, end_points = get_split_array_indexes(self.large_data, n_cpus)
        print("start job pool")
        result = pool.map(work, [(st, end, ind*2+1) for ind, (st,end) in enumerate(
                                                       zip(start_points, end_points))])
        pool.close()
        result = [1]
        print("Done! ",list(result))
    def test(self):
        print (id(self))

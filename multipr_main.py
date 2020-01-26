from multupr_second import CWorker
import numpy as np
# from memory_profiler import memory_usage

# mprof run -M /usr/bin/python3.6 /home/minja/PycharmProjects/3DPredictorTests/multipr_main.py -M -C

if __name__ == '__main__':
    print("Creating data")
    worker = CWorker(np.ones(50000000, dtype=np.float64))
    print(id(worker))
    worker.test()
    print ("Done with data, starting work")
    worker.start_work()
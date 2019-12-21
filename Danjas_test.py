import os,sys
source_path = os.path.join(os.path.dirname(os.path.abspath(os.path.abspath(__file__))),
                           "3Dpredictor/source")
sys.path.append(source_path)
nn_path = os.path.join(os.path.dirname(os.path.abspath(os.path.abspath(__file__))),
                                       "3Dpredictor/nn/source")
sys.path.append(nn_path)

from shared import Interval, Genome
from fastaFileReader import fastaReader
from bigWigFileReader import bigWigReader
from hicFileReader import hicReader
from straw import straw
import numpy as np
import datetime
import logging
logging.basicConfig(level=logging.DEBUG)


def simple_test():
    logging.basicConfig(level=logging.DEBUG) # set to INFO for less detailed output

    ### load data ###
    # load genome
    input_folder = "/home/minja/PycharmProjects/3Dpredictor/nn/input/"
    faReader = fastaReader(input_folder+"hg38/hg38.fa",useOnlyChromosomes=["chr1"])
    faReader = faReader.read_data()
    # load chipSeq
    bwReader1 = bigWigReader(input_folder+"ENCFF473IZV_H1_CTCF.bigWig", genome = faReader, inMemory=True)
    bwReader1 = bwReader1.readData()

    # load chipSeq
    bwReader2 = bigWigReader(input_folder+"ENCFF966IHQ.bigWig", genome = faReader, inMemory=False)
    bwReader2 = bwReader2.readData()


    #load contacts
    resolution = 5000
    hic = hicReader(input_folder+"4DNFI2TK7L2F.hic", genome=faReader, binsize = resolution,
                    indexedData = True)
    hic = hic.read_data()

    ### run simple check that contact count correlate with ChipSeq signal ###

    ### generate some random samples ####
    # get size of the chr1
    total_length = faReader.get_chr_sizes()["chr1"]

    window_size = 20*resolution # distance between intercting regions in this particular test, in units of resolution

    sample_size = 100000

    # select random points on chr1
    random_points_starts = np.random.random_integers(0,
                                              total_length-window_size,
                                              sample_size)
    random_points_starts = np.array((random_points_starts // resolution)*resolution,
                                    dtype = np.uint64)
    random_points_ends = random_points_starts + window_size

    # for each of selected points get contact between this point and (point + window_size*resolution)
    contacts = []
    chipSignals = []
    seqSignals = []
    now = datetime.datetime.now() # start timer

    logging.info("Starting data generation")
    for start,end in zip(random_points_starts,random_points_ends):
        interval = Interval("chr1",start,end)
        contact = hic.get_contact(interval)
        if contact == None:
            continue
        else:
            chipSignal = np.nansum(bwReader1.get_interval(interval))
            if np.isfinite(chipSignal):
                chipSignals.append(chipSignal)
                seqSignal = np.sum(faReader.get_interval(interval))
                seqSignals.append(seqSignal)
                contacts.append(contact)

    logging.info("Time for data generation1: " + str(datetime.datetime.now() - now))
    # now = datetime.datetime.now()
    # chipSignals = []
    # seqSignals = []
    # contacts = []
    # for start,end in zip(random_points_starts,random_points_ends):
    #     interval = Interval("chr1",start,end)
    #     contact = hic.get_contact(interval)
    #     if contact == None:
    #         continue
    #     else:
    #         chipSignal = np.nansum(bwReader2.get_interval(interval))
    #         if np.isfinite(chipSignal):
    #             chipSignals.append(chipSignal)
    #             seqSignal = np.sum(faReader.get_interval(interval))
    #             seqSignals.append(seqSignal)
    #             contacts.append(contact)
    #
    # logging.info("Time for data generation2: " + str(datetime.datetime.now() - now))
    from scipy.stats import spearmanr
    import matplotlib.pyplot as plt

    print(contacts)
    print(chipSignals)

    print (spearmanr(np.array(contacts),np.array(chipSignals)))
    print (np.all(np.isfinite(contacts)))
    print (np.all(np.isfinite(chipSignals)))

    plt.scatter(contacts,chipSignals)
    plt.show()


simple_test()
# coding: utf-8

import csv
import sys
import random
import numpy as np

from collections import defaultdict
from Part1 import *

k = 20
maxt = 1
epsilon = 0.01
st = 0
sv = 0
uarray = 0
varray = 0
bbook = 0


class DataRatingVector(object):
    def __init__(self, size):
        self.len = size
        self.data = [0 for _ in range(size)]
        self.mapping = defaultdict(set)

    def clean(self):
        self.data = [0 for _ in range(self.len)]
        self.mapping = defaultdict(set)

    def randomize(self):
        tmp = [random.randint(0, k - 1) for _ in range(self.len)]
        for itm in range(self.len):  # 'itm' is the data id, 'tmp[itm]' is the cluster id
            self.data[itm] = tmp[itm]
            self.mapping[tmp[itm]] = itm

    def add_data(self, cluster, id_):
        self.data[id_] = cluster
        self.mapping[cluster].add(id_)

    def get_by_cluster(self, cluster):
        return self.mapping[cluster]

    def get_by_id(self, id_):
        return self.data[id_]


def recalcbbook():
    global uarray
    global varray
    global bbook
    global st

    bbook = np.empty(shape=(k, k))
    bbook.fill(0)
    for bi in range(k):
        for bj in range(k):
            usr_set = uarray.get_by_cluster(bi)
            itm_set = varray.get_by_cluster(bj)
            isum = 0
            icount = 0
            for usr in usr_set:
                for itm in itm_set:
                    rating = st.get_rating_by_uid_iid(usr + 1, itm + 1)
                    if rating > 0:
                        isum += rating
                        icount += 1
            if icount == 0:
                bbook[(bi, bj)] = st.avg_rating
            else:
                bbook[(bi, bj)] = isum / icount


def rmse():
    global bbook
    global sv

    #  iterate over sv - for every i,j in sv, find cluster_of_i and cluster_of_j
    #  calculate (bbook[cluster_of_i, cluster_of_j - sv[i,j])**2
    #  sum into total_error, return (total_error / num_of_items)

    total_error = 0
    count = 0

    return total_error / count


def recalc_vector(vec1, vec2):
    global bbook
    global st
    global k

    vec1.clean()
    for i in range(vec1.len):
        newarr = [0 for _ in range(k)]
        for arj in range(k):
            for j in range(vec2.len):
                usrs_cluster = vec2.get_by_id(j)
                a = st.get_rating_by_uid_iid(i + 1, j + 1)
                b = bbook[(arj, usrs_cluster)]
                newarr[arj] += (a - b) ** 2
        new_cluster = np.argmin(newarr)
        vec1.add_data(new_cluster, i)


def recalc_ratings():
    global uarray
    global varray

    t = 1
    lasterror = 99999
    recalcbbook()
    while t <= maxt:
        recalc_vector(uarray, varray)
        recalcbbook()
        recalc_vector(varray, uarray)
        recalcbbook()
        curerror = rmse()
        t += 1
        if lasterror * (1 - epsilon) < curerror:
            t = maxt
    return


def write_to_csv(profiles, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        for row in profiles:
            writer.writerow(row)


def write_dataratingvector_to_csv(vector, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(vector.data)


def main():
    global k
    global maxt
    global epsilon
    global varray
    global uarray
    global st

    if not (len(sys.argv) == 6 or len(sys.argv) == 9) or sys.argv[1] != 'ExtractCB':
        print ('usage: python Part2.py ExtractCB '
               '[the rating input file] [[K size] [T size] [ε size]] [U output directory as csv file] '
               '[V output directory as csv file] [B output directory as csv file]')
        sys.exit(1)
    input_file = ""
    u_output_dir = ""
    v_output_dir = ""
    b_output_dir = ""
    if len(sys.argv) == 6:
        input_file, u_output_dir, v_output_dir, b_output_dir = sys.argv[2:]
    if len(sys.argv) == 9:
        input_file, sk, smaxt, sepsilon, u_output_dir, v_output_dir, b_output_dir = sys.argv[2:]
        k = int(sk)
        maxt = int(smaxt)
        epsilon = float(sepsilon)

    st = Profiles.create(input_file)
    varray = DataRatingVector(len(st._items))
    varray.randomize()
    uarray = DataRatingVector(len(st._users))
    uarray.randomize()

    recalc_ratings()

    print "Writing U vector ..."
    write_dataratingvector_to_csv(uarray, u_output_dir+"UVector.csv")
    print 'DONE'
    print "Writing V vector ..."
    write_dataratingvector_to_csv(varray, v_output_dir+"VVector.csv")
    print 'DONE'
    print "Writing B matrix ..."
    write_to_csv(bbook, b_output_dir+"BMatrix.csv")
    print 'DONE'
    print 'SUCCESS! :-)'


if __name__ == '__main__':
    main()

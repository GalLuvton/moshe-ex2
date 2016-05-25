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
        self._len = size
        self._data = [0 for _ in range(size)]
        self._mapping = defaultdict(set)

    def __len__(self):
        return self._len

    def clean(self):
        self._data = [0 for _ in range(self._len)]
        self._mapping = defaultdict(set)

    def randomize(self):
        global k
        tmp = [random.randint(0, k - 1) for _ in range(self._len)]
        for itm in range(self._len):  # 'itm' is the data id, 'tmp[itm]' is the cluster id
            self._data[itm] = tmp[itm]
            self._mapping[tmp[itm]].add(itm)

    def add_data(self, cluster, id_):
        self._data[id_] = cluster
        self._mapping[cluster].add(id_)

    def get_by_cluster(self, cluster):
        return self._mapping[cluster]

    def get_by_id(self, id_):
        return self._data[id_]

    def to_list(self):
        return self._data


def recalcbbook():
    global k
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
                    rating = st.get_rating_by_uid_iid(usr + 1, itm + 1)  # TODO - rename to whatever it really is
                    if rating > 0:
                        isum += rating
                        icount += 1
            if icount == 0:
                bbook[(bi, bj)] = st.avg_rating
            else:
                bbook[(bi, bj)] = isum / icount


def rmse():
    global uarray
    global varray
    global bbook
    global sv

    total_error = 0
    count = 0

    for (usr, itm, rating) in sv.getsomethingawesome:  # TODO - rename to whatever it really is
        usr_cluster = uarray.get_by_id(usr)
        itm_cluster = varray.get_by_id(itm)
        total_error += (bbook[usr_cluster, itm_cluster] - rating)**2
        count += 1

    return total_error / count


def recalc_vector(vec1, vec2):
    global k
    global bbook
    global st

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
    global maxt
    global epsilon
    global uarray
    global varray

    t = 1
    curerror = 0
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
            break

    return t, curerror


def write_to_csv(profiles, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        for row in profiles:
            writer.writerow(row)


def write_dataratingvector_to_csv(vector, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(vector.to_list())


def main():
    global k
    global maxt
    global epsilon
    global uarray
    global varray
    global st
    global sv

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

    st, sv, p, q = Profiles.create(input_file).split_20_80()
    uarray = DataRatingVector(p)
    uarray.randomize()
    varray = DataRatingVector(q)
    varray.randomize()

    t, err = recalc_ratings()
    print 'Finished after %d iterations (out of %d), with an error of %f' % (t, maxt, err)

    output_file = u_output_dir+"UVector.csv"
    print "Writing U vector to '%s' ..." % output_file
    write_dataratingvector_to_csv(uarray, output_file)
    print 'DONE'
    output_file = v_output_dir+"VVector.csv"
    print "Writing V vector to '%s' ..." % output_file
    write_dataratingvector_to_csv(varray, output_file)
    print 'DONE'
    output_file = b_output_dir+"BMatrix.csv"
    print "Writing B matrix to '%s'..." % output_file
    write_to_csv(bbook, output_file)
    print 'DONE'


if __name__ == '__main__':
    main()

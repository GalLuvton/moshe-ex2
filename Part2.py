# coding: utf-8

import csv
import sys
import random
import numpy as np

from collections import defaultdict
from Part1 import *

q = 0
p = 0
k = 20
maxt = 1
epsilon = 0.01
varray = {}
uarray = {}
bbook = {}
st = {}


def recalcbbook():
    tmpbbook = np.empty(shape=(k, k))
    tmpbbook.fill(0)
    for bi in range(k):
        for bj in range(k):
            usr_set = uarray[bi]
            itm_set = varray[bj]
            isum = 0
            icount = 0
            for usr in usr_set:
                for itm in itm_set:
                    rating = st.get_rating_by_uid_iid(usr + 1, itm + 1)
                    if rating > 0:
                        isum += rating
                        icount += 1
            if icount != 0:
                tmpbbook[(bi, bj)] = isum / icount
    return tmpbbook


def rmse():
    totalerror = 0
    usrcount = 0
    new_uarray = defaultdict(set)
    for _, cluster in uarray.iteritems():
        for usr in cluster:
            user_ratings = st.get_user_by_id(usr+1)
            errormin = 99999
            cur_user_cluster = 0
            for ti in range(k):
                tcurerror = 0
                flagset = 0
                for itmkey, value in user_ratings._attr_rating_pairs():
                    itm_cluster = 0
                    for clst, tcluster in varray.iteritems():
                        if itmkey in tcluster:
                            itm_cluster = clst
                            break
                    a = st.get_rating_by_uid_iid(value + 1, itmkey + 1)
                    b = bbook[(ti, itm_cluster)]
                    if a > 0 and b > 0:
                        flagset = 1
                        tcurerror += (a - b) ** 2
                if flagset and tcurerror < errormin:
                    errormin = tcurerror
                    cur_user_cluster = ti
            new_uarray[cur_user_cluster].add(usr)
            totalerror += errormin
            usrcount += 1
    global uarray
    uarray = new_uarray
    return totalerror / usrcount


def recalc_ratings():
    global bbook
    t = 1
    lasterror = 99999
    bbook = recalcbbook()
    while t <= maxt:
        new_uarray = defaultdict(set)
        for i in range(p):
            newarr = [0 for _ in range(k)]
            for arj in range(k):
                for j in range(q):
                    usrs_cluster = 0
                    for clst, cluster in varray.iteritems():
                        if j in cluster:
                            usrs_cluster = clst
                            break
                    a = st.get_rating_by_uid_iid(i + 1, j + 1)
                    b = bbook[(arj, usrs_cluster)]
                    newarr[arj] += (a - b) ** 2
            new_cluster = np.argmin(newarr)
            new_uarray[new_cluster].add(i)
        global uarray
        uarray = new_uarray
        bbook = recalcbbook()
        new_varray = defaultdict(set)
        for j in range(q):
            newarr = [0 for _ in range(k)]
            for arj in range(k):
                for i in range(p):
                    usrs_cluster = 0
                    for clst, cluster in uarray.iteritems():
                        if i in cluster:
                            usrs_cluster = clst
                            break
                    a = st.get_rating_by_uid_iid(i + 1, j + 1)
                    b = bbook[(usrs_cluster, arj)]
                    newarr[arj] += (a - b) ** 2
            new_cluster = np.argmin(newarr)
            new_varray[new_cluster].add(j)
        global varray
        varray = new_varray
        bbook = recalcbbook()
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


def write_set_to_csv(vector, len, filename):
    flat_arr = [0 for _ in range(len)]
    for clst, cluster in vector.iteritems():
        for eid in cluster:
            flat_arr[eid] = clst
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(flat_arr)


def main():
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
        global k
        global maxt
        global epsilon
        input_file, sk, smaxt, sepsilon, u_output_dir, v_output_dir, b_output_dir = sys.argv[2:]
        k = int(sk)
        maxt = int(smaxt)
        epsilon = float(sepsilon)

    global st
    st = Profiles.create(input_file)

    global q
    q = len(st._items)
    global p
    p = len(st._users)
    global varray
    tmparray = [random.randint(0, k - 1) for _ in range(q)]
    varray = defaultdict(set)
    for i in range(q):
        varray[tmparray[i]].add(i)  # 'i' being userId, tmparray[i] being its cluster
    global uarray
    tmparray = [random.randint(0, k - 1) for _ in range(q)]
    uarray = defaultdict(set)
    for i in range(q):
        uarray[tmparray[i]].add(i)  # 'i' being itemId, tmparray[i] being its cluster

    recalc_ratings()

    print "Writing U vector ..."
    write_set_to_csv(uarray, p, u_output_dir+"UVector.csv")
    print 'DONE'
    print "Writing V vector ..."
    write_set_to_csv(varray, q, v_output_dir+"VVector.csv")
    print 'DONE'
    print "Writing B matrix ..."
    write_to_csv(bbook, b_output_dir+"BMatrix.csv")
    print 'DONE'
    print 'SUCCESS! :-)'


if __name__ == '__main__':
    main()

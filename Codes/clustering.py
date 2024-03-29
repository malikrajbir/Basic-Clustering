#!/usr/bin/env python3
"A program to generate a set of random points and use the for clustering."

import sys
from random import choice, randint
from point_class import point
from math import sqrt
from matplotlib import pyplot as plt

try:
    from tqdm import trange
    __it = lambda x : trange(x)
    print('Using: trange')
except ImportError:
    from itertools import repeat
    __it = lambda x : repeat(None, x)
    print('Using: repeat')


def all_true(bool_list):
    answer = True
    for case in bool_list:
        answer = answer and case
    return answer

def closest(pnt, cluster_pivots):
    min_dist_point = len(cluster_pivots)-1
    min_dist = pnt.distance(cluster_pivots[min_dist_point])
    i = 0
    while i < len(cluster_pivots)-1:
        if pnt.distance(cluster_pivots[i]) < min_dist:
            min_dist_point = i
            min_dist = pnt.distance(cluster_pivots[i])
        i += 1
    return min_dist_point

def get_mean(point_list):
    total_x = 0
    total_y = 0
    for pnt in point_list:
        total_x += pnt.x()
        total_y += pnt.y()
    return point(total_x/len(point_list), total_y/len(point_list))

def write_list_string(point_list):
    _s = ""
    for pnt in point_list:
        _s = _s+str(pnt.x())+" "+str(pnt.y())+"\n"
    return _s

def get_points_from_file(file):
    file.readline()
    file.readline()
    points = []
    for line in file:
        if line == '\n':
            break
        points.append(point(int(line.split()[0]), int(line.split()[-1])))
    return points

def get_points(case):
    if case == 0:
        _f = open("../Distributions/uniform_"+sys.argv[3]+".txt")
    elif case == 1:
        _f = open("../Distributions/point_square_"+sys.argv[3]+"_"+sys.argv[4]+"_"+sys.argv[5]+".txt")
    elif case == 2:
        _f = open("../Distributions/point_circle_"+sys.argv[3]+"_"+sys.argv[4]+"_"+sys.argv[5]+".txt")
    elif case == 3:
        _f = open("../Distributions/concentric_circles_"+sys.argv[3]+"_"+sys.argv[4]+".txt")
    elif case == 4:
        _f = open("../Distributions/random_lines_"+sys.argv[3]+"_"+sys.argv[4]+".txt")
    elif case == 5:
        _f = open("../Distributions/random_polynomial_"+sys.argv[3]+"_"+sys.argv[4]+"_"+sys.argv[5]+".txt")
    else:
        print("Illegal Case")
        sys.exit(0)
    return get_points_from_file(_f)

def random_pivots(points):
    cluster_pivots = []
    while len(cluster_pivots) != int(sys.argv[1]):
        temp_point = choice(points)
        if cluster_pivots.count(temp_point) == 0:
            cluster_pivots.append(temp_point)
    return cluster_pivots

def Jovian(cls, pts):
    _dist = 0
    for i in range(len(cls)):
        _cl = cls[i]
        _pvt = pts[i]
        for _pt in _cl:
            _dist += (_pt.distance(_pvt)**2)
    return sqrt(_dist)

def main():
    case = int(sys.argv[2])

    total_clusters = int(sys.argv[1])

    points = get_points(case)

    clusters = [[] for _ in range(total_clusters)]
    cluster_pivots = random_pivots(points)
    min_heuristic = -1
    cluster_complete = [False]*total_clusters
    best_fit = []

    for _ in __it(20*total_clusters):
        while True:
            for pnt in points:
                clusters[closest(pnt, cluster_pivots)].append(pnt)
            for i in range(total_clusters):
                if not cluster_complete[i]:
                    mean_point = get_mean(clusters[i])
                    if mean_point.distance(cluster_pivots[i]) <= pow(10, -4):
                        cluster_complete[i] = True
                    cluster_pivots[i] = mean_point
            if all_true(cluster_complete):
                break
            clusters = [[] for _ in range(total_clusters)]
        _heuristic = Jovian(clusters, cluster_pivots)
        if min_heuristic == -1 or _heuristic < min_heuristic:
            min_heuristic = _heuristic
            best_fit = clusters
        clusters = [[] for _ in range(total_clusters)]
        cluster_pivots = random_pivots(points)

    for cluster in best_fit:
        r = lambda: randint(0,255)
        clr = ('#%02X%02X%02X' % (r(),r(),r()))
        x = []
        y = []
        for pnt in cluster:
            x.append(pnt.x())
            y.append(pnt.y())
        plt.plot(x, y, 'o', markersize = 2, color = clr)
    plt.show()

if __name__ == '__main__':
    main()

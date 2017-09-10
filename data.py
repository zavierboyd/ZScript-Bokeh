import csv

with open('globalwarmingsims/rcp3-1765-2100.csv', 'r') as f:
    reader = csv.DictReader(f)
    rcp3data = [row for row in reader]
    # rcp3data = [[float(num) for num in line.strip().split(',')] for line in f.readlines()]
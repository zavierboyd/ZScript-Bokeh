import csv

with open('rcp3-1765-2200co.csv', 'r') as f:
    reader = csv.DictReader(f)
    rcp3codata = {int(row['year']): row for row in reader}

with open('rcp3-1765-2200rf.csv', 'r') as f:
    reader = csv.DictReader(f)
    rcp3rfdata = {int(row['year']): row for row in reader}

with open('rcp6-1765-2200rf.csv', 'r') as f:
    reader = csv.DictReader(f)
    rcp6rfdata = {int(row['year']): row for row in reader}

with open('rcp6-1765-2200co.csv', 'r') as f:
    reader = csv.DictReader(f)
    rcp6codata = {int(row['year']): row for row in reader}

with open('rcp4.5-1765-2200rf.csv', 'r') as f:
    reader = csv.DictReader(f)
    rcp45rfdata = {int(row['year']): row for row in reader}

with open('rcp4.5-1765-2200rf.csv', 'r') as f:
    reader = csv.DictReader(f)
    rcp45codata = {int(row['year']): row for row in reader}

with open('rcp8.5-1765-2200rf.csv', 'r') as f:
    reader = csv.DictReader(f)
    rcp85rfdata = {int(row['year']): row for row in reader}

with open('rcp8.5-1765-2200co.csv', 'r') as f:
    reader = csv.DictReader(f)
    rcp85codata = {int(row['year']): row for row in reader}

import csv
from entities import Person
csv_line = []
max_floors = 6

with open(r"C:\Users\tampo\OneDrive\Documents\School\Year 1\csc148\csc148\assignments\a1\sample_arrivals.csv") as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        for i in range(len(line)):
            line[i] = int(line[i])
        csv_line.append(line)

round_at = []
mapper = {}
for i in range(max_floors):
    mapper[i] = []

for i in csv_line:
    round_at = i
    if round_at[0] == 1:
        for j in range(2, len(round_at), 2):
            mapper[1].append(Person(round_at[j - 1], round_at[j]))

print(mapper[1][0].start)
print(mapper[1][0].target)
print(mapper[1][1].start)
print(mapper[1][1].target)

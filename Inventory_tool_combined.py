import csv

data = open('raw-locations.csv', 'r')
#data = open('inv_loc_1.csv', 'r')

reader = csv.reader(data)

#ls_data = [x for x in sorted([[y for y in line if y] for line in reader], key=lambda x: len([y for y in x if y])) if x]
ls_data = [line for line in reader]

print(ls_data[0])
print()


building_sql = []
floor_sql = []
room_sql = []
storage_sql = []
rack_sql = []

hierarchy = {
    0: 'Building',
    1: 'Floor',
    2: 'Room',
    3: 'Storage',
    4: 'Rack',
}

capacity = {
    'Building': '0,-1',
    'Floor': '0,-1',
    'Room': '-1,-1',
    'Storage': '-1,-1',
    'Rack': '100,-1',
}

lists = {
    0: building_sql,
    1: floor_sql,
    2: room_sql,
    3: storage_sql,
    4: rack_sql
}

for row in ls_data:
    for n in range(5):
        lists[n].append(
        "execute inv_upload.invupd('{}','{}','{}','{}','{}')".format(hierarchy[n],
                                                                     row[n+1],
                                                                     capacity[hierarchy[n]],
                                                                     '-'.join([row[x + 1] for x in range(n + 1)]),
                                                                     ':'.join([row[x] for x in range(n + 1)])
                                                                     ))



for l in storage_sql:
    print(l)

#execute inv_upload.invupd('Building','B84',0,-1,'B84','FM-AD-AD-EMEA-DE-MO');
#execute inv_upload.invupd('Floor','2.OG',0,-1,'B40-2.OG','FM-AD-AS-EMEA-DE-MO:B40');
#execute inv_upload.invupd('Room','02',-1,-1,'B40-EG-02','FM-AD-AD-EMEA-DE-MO:B40:EG');
#execute inv_upload.invupd('Storage','Bench06',-1,-1,'B40-2.OG-09-Bench06','FM-AD-AD-EMEA-DE-MO:B40:2.OG:09');
#execute inv_upload.invupd('Rack','Shelf02',100,-1,'B84-EG-LsmCon-SafetyContainer-Shelf02','FM-AD-AD-EMEA-DE-MO:B84:EG:LsmCon:SafetyContainer');


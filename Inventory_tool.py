import csv
import argparse

# Set up hierarchical SQL divisions
building_sql = []
floor_sql = []
room_sql = []
storage_sql = []
rack_sql = []

# Set up value dictionaries - can be edited and SQL will still be correctly generated
hierarchy = {
    0: 'Building',
    1: 'Floor',
    2: 'Room',
    3: 'Storage',
    4: 'Rack',
}
capacity = {
    0: [0, -1],
    1: [0, -1],
    2: [-1, -1],
    3: [-1, -1],
    4: [100, -1]
}
lists = {
    0: building_sql,
    1: floor_sql,
    2: room_sql,
    3: storage_sql,
    4: rack_sql
}


def write_sql(ls_data, out, *args):
        # Dynamic SQL generation
    for row in ls_data:
        if row[0] == '':
            continue
        for n in range(5):
            if args[0]:
                if len(row) == 1:
                    continue
                else:
                    n = len(row)-2
            sql = "execute inv_upload.invupd('{}','{}',{}, {},'{}','{}');".format(hierarchy[n],
                                                                                  row[n+1],
                                                                                  capacity[n][0], capacity[n][1],
                                                                                  '-'.join([row[x + 1]
                                                                                            for x in range(n + 1)
                                                                                            if row[x + 1]]),
                                                                                  ':'.join([row[x]
                                                                                            for x in range(n + 1)
                                                                                            if row[x]]))
            if sql not in lists[n]:
                lists[n].append(sql)
    if not args[1]:
        levels = 5
    else:
        levels = args[1]
    for x in range(levels):
        for row in lists[x]:
            print(row, file=out)
    out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Please provide file path...')
    parser.add_argument('locations', help='The csv file of locations')
    parser.add_argument('--h', action='store_true', help='Specify file paths are stored in hierarchy - legacy format')
    parser.add_argument('--s', type=int, help='Specify single level in heirarchy')

    ags = parser.parse_args()

    # File handling
    data = open(ags.locations, 'r')

    reader = csv.reader(data)
    if ags.h:
        loc_data = [x for x in sorted([[y for y in line if y] for line in reader],
                                      key=lambda x: len([y for y in x if y])) if x]
    else:
        loc_data = [line for line in reader]
    output = open('sql_out.txt', 'w')

    write_sql(loc_data, output, ags.h, ags.s)

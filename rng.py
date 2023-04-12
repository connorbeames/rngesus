import pandas as pd
import json
import random

chest_patterns = 65536
# rune_patterns = []

# opening odds file
with open('odds.json') as json_file:
    runes = json.load(json_file)

'''
Used when the rune_patterns.json has not been initialized
Will auto assign chest patterns to rune drops fitting with how many
patterns there are per rune.
'''
# for rune in runes:
#     i = 0
#     rune_id = rune['rune_id']
#     rune_name = rune['rune']
#     while i < rune['drop rate']:
#         randomnumber = random.randint(1, chest_patterns)
#         rune_patterns.append({"rune_id": rune_id, "rune_name": rune_name, "pattern_id": randomnumber})
#         i = i + 1

# with open('rune_patterns.json', 'w') as fout:
#     json.dump(rune_patterns, fout)

# opening runes file
with open('rune_patterns.json') as rune_patterns_json_file:
    rune_patterns_list = json.load(rune_patterns_json_file)

run_lk_loop = 'yes'

time_to_run = int(input('\nEnter the number of seconds it takes you to run Lower Kurast: '))

while run_lk_loop == 'yes':
    pattern_ids = []
    for pattern in rune_patterns_list:
        pattern_ids.append(pattern['pattern_id'])

    rune_drops = []
    last_drop = 0
    runs = input('\nEnter the number of Lower Kurast runs: ')
    run_total = int(runs)
    time_spent = float(runs) * time_to_run / 60 / 60

    a = 0
    while a < run_total:
        i = 0
        a = a + 1
        while i < 6:
            i = i + 1
            randomnumber = random.randint(1, chest_patterns)
            isPresent = randomnumber in pattern_ids
            if isPresent == True:
                runs_since_last_drop = (a - last_drop)
                time_to_drop = float(runs_since_last_drop) * time_to_run / 60 / 60
                time_to_drop = str(f"{round(time_to_drop,1)}hr")
                total_time = str(f"{round(float(a) * time_to_run / 60 / 60, 1)}hr")
                rune_drops.append({"run_number": a, "runs_since_last_drop": runs_since_last_drop, "time_to_drop": time_to_drop, "total_time": total_time, "pattern_id": randomnumber})
                last_drop = a

    if len(rune_drops) == 0:
        print(f"\nWith an average run of {time_to_run} seconds, you spent {round(time_spent,2)} hours.")
        print("\nSucks to suck, you didn't find any runes.")
    else:
        df_rune_patterns = pd.DataFrame.from_records(rune_patterns_list)
        df_rune_drops = pd.DataFrame.from_records(rune_drops)
        df_runes = pd.DataFrame.from_records(runes)

        mergedData1 = df_rune_drops.merge(df_rune_patterns, on='pattern_id')
        mergedData2 = mergedData1.merge(df_runes, on='rune_id')
        mergedData2.columns = ['Run Number', 'Runs to Drop', 'Time to Drop', 'Total Time', 'Pattern Id', 'Rune Id', 'Rune Name', 'Rune', 'Drop Rate']
        del mergedData2["Rune Name"]
        del mergedData2["Pattern Id"]
        mergedData2.sort_values(by=['Run Number'], inplace=True)

        print(f"\nWith an average run of {time_to_run} seconds, you spent {round(time_spent,2)} hours.")
        print("\nYou found some runes! Here are your results:")
        print(mergedData2)

    run_lk_loop = input('\nWould you like to continue your addiction (Yes/No): ')
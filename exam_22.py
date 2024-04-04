from collections import Counter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

from utils import adjust_labels, plot_bargraph

TRIES = 0
POINTS = 1


def calculate_scores(data, filtered):
    if filtered:
        data = data.sort_values(by='sum', axis=1, ascending=False)
        data = data.iloc[:, 33:-33]
    row_headers = data.index.tolist()
    categories = [elem[:-2] for elem in row_headers[:-1:3]]
    participant_ids = data.columns.tolist()
    res_dict = {category: [0, 0] for category in categories}
    # participants with 3 or more categories with 0 points
    # participants_with_0 = []
    # participants_with_pts = []
    for participant in participant_ids:
        # categories_with_0 = 0
        # categories_with_pts = 0
        for category in categories:
            tot_points = 0
            for i in range(3):
                value = float(data.loc[f'{category}_{i}', participant])
                tot_points += value
            if tot_points > 0:
                res_dict[category][TRIES] += 1
                res_dict[category][POINTS] += tot_points
            #     categories_with_pts += 1
            # else:
            #     categories_with_0 += 1
        # if categories_with_0 >= 3:
        #     participants_with_0.append(participant)
        # if categories_with_pts > 6:
        #     participants_with_pts.append(participant)
    return res_dict


def average_score(res_dict):
    avg_points = {category: res_dict[category][POINTS] / res_dict[category][TRIES] for category in res_dict.keys()}
    avg_points = dict(sorted(avg_points.items(), key=lambda item: item[1], reverse=True))
    return avg_points




def main():
    # replace , with . in exam_results_2022.tsv file before using read_csv
    data_file = open('csv/exam_results_2022.tsv', 'r')
    data_tmp = open('csv/exam_results_2022_tmp.tsv', 'w')
    # replace all commas with dots in data_tmp
    for line in data_file:
        data_tmp.write(re.sub(r',', r'.', line))
    data_file.close()
    data_tmp.close()
    data = pd.read_csv('csv/exam_results_2022_tmp.tsv', sep='\t', index_col=0)
    filtered_data = average_score(calculate_scores(data, True))
    unfiltered_data = average_score(calculate_scores(data, False))
    # split keys on _ and capitalize each word and add it to a list using list comprehension
    filtered_keys = [' '.join(key.split('_')).capitalize() for key in filtered_data.keys()]
    unfiltered_keys = [' '.join(key.split('_')).capitalize() for key in unfiltered_data.keys()]
    filtered_values = list(filtered_data.values())
    unfiltered_values = list(unfiltered_data.values())

    plot_bargraph(unfiltered_keys, unfiltered_values, "Avg scores", "Exam results unfiltered", "unfiltered_exam_results")
    plot_bargraph(filtered_keys, filtered_values, "Avg scores", "Exam results filtered", "filtered_exam_results")

    filtered_data = calculate_scores(data, True)

    filtered_keys = [' '.join(key.split('_')).capitalize() for key in filtered_data.keys()]
    filtered_values = [list(filtered_data.values())[i][TRIES] for i in range(len(filtered_data.values()))]

    # Pair each key with its corresponding value
    paired = list(zip(filtered_keys, filtered_values))

    # Sort the paired list based on the values
    paired_sorted = sorted(paired, key=lambda x: x[1], reverse=True)

    # Extract the keys and values back into separate lists
    filtered_keys = [item[0] for item in paired_sorted]
    filtered_values = [item[1] for item in paired_sorted]

    plot_bargraph(filtered_keys, filtered_values, "Attempts", "Exam results filtered", "filtered_exam_results_attempts")
    # filtered_values = list(filtered_data.values()[TRIES])

    unfiltered_data = calculate_scores(data, False)
    print(unfiltered_data)
    unfiltered_keys = [' '.join(key.split('_')).capitalize() for key in unfiltered_data.keys()]
    unfiltered_values = [list(unfiltered_data.values())[i][TRIES] for i in range(len(unfiltered_data.values()))]

    # Pair each key with its corresponding value
    paired = list(zip(unfiltered_keys, unfiltered_values))

    # Sort the paired list based on the values
    paired_sorted = sorted(paired, key=lambda x: x[1], reverse=True)

    # Extract the keys and values back into separate lists
    unfiltered_keys = [item[0] for item in paired_sorted]
    unfiltered_values = [item[1] for item in paired_sorted]

    plot_bargraph(unfiltered_keys, unfiltered_values, "Attempts", "Exam results unfiltered", "unfiltered_exam_results_attempts")





if __name__ == "__main__":
    main()

from collections import Counter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

from utils import adjust_labels

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


def plot_bargraph(keys, values):
    keys = adjust_labels(keys)
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 8))
    bar_graph = sns.barplot(x=keys, y=values)
    bar_graph.set_ylabel("Average Points filtered")
    start = min(values) - 1
    end = max(values) + 1
    plt.ylim(start, end)
    plt.show()


def main():
    # replace , with . in exam_results_2022.tsv file before using read_csv
    data_file = open('exam_results_2022.tsv', 'r')
    data_tmp = open('exam_results_2022_tmp.tsv', 'w')
    # replace all commas with dots in data_tmp
    for line in data_file:
        data_tmp.write(re.sub(r',', r'.', line))
    data_file.close()
    data_tmp.close()
    data = pd.read_csv('exam_results_2022_tmp.tsv', sep='\t', index_col=0)
    filtered_data = average_score(calculate_scores(data, True))
    unfiltered_data = average_score(calculate_scores(data, False))
    # split keys on _ and capitalize each word and add it to a list using list comprehension
    filtered_keys = [' '.join(key.split('_')).capitalize() for key in filtered_data.keys()]
    unfiltered_keys = [' '.join(key.split('_')).capitalize() for key in unfiltered_data.keys()]
    filtered_values = list(filtered_data.values())
    unfiltered_values = list(unfiltered_data.values())

    # plot_bargraph(filtered_keys, filtered_values)
    # plot_bargraph(unfiltered_keys, unfiltered_values)

    filtered_data = calculate_scores(data, True)

    filtered_keys = [' '.join(key.split('_')).capitalize() for key in filtered_data.keys()]
    filtered_values = [list(filtered_data.values())[i][TRIES] for i in range(len(filtered_data.values()))]
    plot_bargraph(filtered_keys, filtered_values)
    # filtered_values = list(filtered_data.values()[TRIES])




if __name__ == "__main__":
    main()

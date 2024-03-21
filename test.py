import pandas as pd
from scipy.stats import f_oneway, ttest_ind
import numpy as np

def load_data(file_path):
    """
    Loads data from a tab-separated values file.

    Parameters:
    - file_path (str): The path to the file containing the data.

    Returns:
    - DataFrame: A pandas DataFrame containing the loaded data.
    """
    return pd.read_csv(file_path, delimiter='\t', index_col=0)

def calculate_correct_answers(data, start_col, end_col):
    """
    Calculates which answers are correct based on a row of correct answers.

    Parameters:
    - data (DataFrame): The DataFrame containing the test data.
    - start_col (str): The name of the first column of answer data.
    - end_col (str): The name of the last column of answer data.

    Returns:
    - DataFrame: A DataFrame indicating True for correct answers and False for incorrect answers.
    """
    correct_answers = data.loc['correct_answers', start_col:end_col]
    participant_answers = data.loc['0':, start_col:end_col]
    results_individual = participant_answers.apply(lambda x: (x == correct_answers), axis=1)
    return results_individual

def calculate_mean(results_individual):
    """
    Calculates the mean score for each participant.

    Parameters:
    - results_individual (DataFrame): A DataFrame where each row represents a participant and each column a question,
      with True for correct answers and False for incorrect ones.

    Returns:
    - ndarray: An array containing the mean score for each participant.
    """
    mean_participant = results_individual.mean(axis=1)
    mean_participant_array = mean_participant.to_numpy()
    return mean_participant_array

def perform_one_way_anova(results_individual):
    """
    Performs a one-way ANOVA test on the given data.

    Parameters:
    - results_individual (DataFrame): A DataFrame where each row represents a participant and each column a question,
      with integer values (1 for correct, 0 for incorrect).

    Returns:
    - F_onewayResult: The result of the ANOVA test, including F-statistic and p-value.
    """
    results_individual = results_individual.astype(int).T
    return f_oneway(*results_individual.values)

def calculate_variance(mean_participant_array):
    """
    Calculates the variance of the mean scores for participants.

    Parameters:
    - mean_participant_array (ndarray): An array containing the mean score for each participant.

    Returns:
    - float: The variance of the mean participant scores.
    """
    return np.var(mean_participant_array)

def perform_t_test(array1, array2):
    """
    Performs Welch's t-test on two arrays of scores.

    Parameters:
    - array1 (ndarray): The first set of scores.
    - array2 (ndarray): The second set of scores.

    Returns:
    - tuple: A tuple containing the T-statistic and the p-value of the test.
    """
    t_stat, p_value = ttest_ind(array1, array2, equal_var=False)
    return t_stat, p_value

def main():
    category = 'virt'
    data_2024 = load_data('csv/resultater24.tsv')
    results_individual_2024 = calculate_correct_answers(data_2024, f'q1_{category}', f'q5_{category}')
    mean_participant_2024_array = calculate_mean(results_individual_2024)
    # one_way_anova_2024 = perform_one_way_anova(results_individual_2024)

    data_2023 = load_data('csv/resultater23_v2.tsv')
    results_individual_2023 = calculate_correct_answers(data_2023, f'q1_{category}', f'q5_{category}')
    mean_participant_2023_array = calculate_mean(results_individual_2023)
    # one_way_anova_2023 = perform_one_way_anova(results_individual_2023)

    t_stat, p_value = perform_t_test(mean_participant_2024_array, mean_participant_2023_array)
    print("T-statistic:", t_stat)
    print("P-value:", p_value)

    #print both mean arrays nicely formatted
    print("Mean participant scores for 2024:")
    for i, score in enumerate(mean_participant_2024_array):
        print(f"Participant {i + 1}: {score}")
    print("Mean participant scores for 2023:")
    print(mean_participant_2023_array)

    return

    seen_animation = results.loc[data_2024.loc[results.index, 'mange_i_snitt_animert_proc'] != '0']
    not_seen_animation = results.loc[data_2024.loc[results.index, 'mange_i_snitt_animert_proc'] == '0']

    seen_animation_not_lecture = results.loc[
        (data_2024.loc[results.index, 'mange_i_snitt_animert_proc'] != '0') &
        (data_2024.loc[results.index, 'mange_videoer_proc'] == '0')
        ]
    print(seen_animation_not_lecture)

    seen_lecture_not_animation = results.loc[
        (data_2024.loc[results.index, 'mange_i_snitt_animert_proc'] == '0') &
        (data_2024.loc[results.index, 'mange_videoer_proc'] != '0')
        ]
    print(len(seen_lecture_not_animation))

    seen_animation_and_lecture = results.loc[
        (data_2024.loc[results.index, 'mange_i_snitt_animert_proc'] != '0') &
        (data_2024.loc[results.index, 'mange_videoer_proc'] != '0')
        ]

    not_seen_any = results.loc[
        (data_2024.loc[results.index, 'mange_i_snitt_animert_proc'] == '0') &
        (data_2024.loc[results.index, 'mange_videoer_proc'] == '0')
        ]

    print(f'Average score for those who have seen the animation:\t\t\t\t\t {seen_animation_not_lecture.mean()}')
    print(f'Average score for those who have not seen the animation:\t\t\t\t {seen_lecture_not_animation.mean()}')
    print(f'Average score for those who have seen the animation and the lecture:\t {seen_animation_and_lecture.mean()}')
    print(f'Average score for those who have not seen the animation or the lecture:\t {not_seen_any.mean()}')
    print()
    print(f'Number of participants who have seen the animation:\t\t\t\t\t\t {len(seen_animation_not_lecture)}')
    print(f'Number of participants who have not seen the animation:\t\t\t\t\t {len(seen_lecture_not_animation)}')
    print(f'Number of participants who have seen the animation and the lecture:\t\t {len(seen_animation_and_lecture)}')
    print(f'Number of participants who have not seen the animation or the lecture:\t {len(not_seen_any)}')

    # len all
    print(
        len(seen_animation_not_lecture) +
        len(seen_lecture_not_animation) +
        len(seen_animation_and_lecture) +
        len(not_seen_any)
    )


if __name__ == "__main__":
    main()

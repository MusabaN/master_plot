import pandas as pd
from scipy.stats import f_oneway, ttest_ind
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from textwrap import dedent


def load_data(file_path):
    """
    Loads data from a tab-separated values file.

    Parameters:
    - file_path (str): The path to the file containing the data.

    Returns:
    - DataFrame: A pandas DataFrame containing the loaded data.
    """
    dataframe = pd.read_csv(file_path, delimiter='\t', index_col=0)

    # Check if '0' exists in the DataFrame index to avoid errors
    if '0' in dataframe.index:
        # Apply the replacement and conversion only from row '0' onwards
        dataframe.loc['correct_answers':, :] = dataframe.loc['correct_answers':, :].replace("-", np.nan)
        dataframe.loc['correct_answers':, :] = dataframe.loc['correct_answers':, :].apply(pd.to_numeric, errors='coerce')

    return dataframe


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
    t_stat, p_value = ttest_ind(array1, array2, equal_var=True)
    return t_stat, p_value


def filter_out_not_seen_animation(data_2024, results_individual_2024, category):
    return results_individual_2024.loc[
        data_2024.loc[results_individual_2024.index, f'mange_i_snitt_animert_{category}'] != '0']


def plot_comparison_graph(data_2023, data_2024, postpend='proc', save_name='comparison'):
    first_participant = data_2024.index[3]
    correct_answers = data_2024.loc['correct_answers', f'q1_{postpend}':f'q5_{postpend}'].to_list()
    res_2024 = data_2024.loc[first_participant:, f'q1_{postpend}':f'q5_{postpend}'].apply(lambda x: (x == correct_answers).sum(), axis=1)
    dist_2024 = res_2024.value_counts(normalize=True).mul(100).round(2).reindex(range(6)).sort_index()

    first_participant = data_2023.index[3]
    res_2023 = data_2023.loc[first_participant:, f'q1_{postpend}':f'q5_{postpend}'].apply(lambda x: (x == correct_answers).sum(), axis=1)
    dist_2023 = res_2023.value_counts(normalize=True).mul(100).round(2).reindex(range(6)).sort_index()

    print(save_name + " " + postpend + " 2024:\t" + str(res_2024.mean().round(2)))
    print(save_name + " " + postpend + " 2023:\t" + str(res_2023.mean().round(2)))

    return

    df = pd.DataFrame({
        'Points': dist_2023.index,  # Assuming the index is 0 to 5
        '2023': dist_2023.values,
        '2024': dist_2024.values
    })

    # Melt the DataFrame to long format
    df_long = pd.melt(df, id_vars=['Points'], value_vars=['2023', '2024'], var_name='Year', value_name='Percentage')

    # Load the "muted" palette
    palette = sns.color_palette("muted")

    # Access specific colors, for example, the first (index 0) and third (index 2) colors
    color_for_2023 = palette[0]
    color_for_2024 = palette[1]

    # Example of using these colors in a plot
    sns.set_style(style='whitegrid')
    plt.figure(figsize=(10, 6))
    # Assume 'df_long' is your DataFrame prepared for plotting
    sns.barplot(x='Points', y='Percentage', hue='Year', data=df_long, palette=[color_for_2023, color_for_2024])

    # Adding mean lines with the selected colors
    # plt.axhline(y=dist_2023.mean(), color=color_for_2023, linestyle='--', label=f'Mean 2023: {dist_2023.mean():.2f}')
    # plt.axhline(y=dist_2024.mean(), color=color_for_2024, linestyle='--', label=f'Mean 2024: {dist_2024.mean():.2f}')

    # Other plot settings
    plt.xlabel('Points Scored')
    plt.ylabel('Percentage of Students')
    plt.title('Comparison of Student Scores by Year')
    plt.legend(title='Year')

    # Show the plot
    plt.savefig(f'./plots/comparison_{postpend}_{save_name}.png')


def main():
    postpend = 'virt'
    data_2024 = load_data('csv/resultater24.tsv')
    data_2023 = load_data('csv/resultater23.tsv')
    # data_2024 = data_2024.loc[data_2024.loc[data_2024.index, f'mange_i_snitt_animert_{postpend}'] != 0]
    # data_2023 = data_2023.loc[data_2023.loc[data_2023.index, f'mange_i_snitt_{postpend}'] != 0]

    # question_list = data_2024.loc[:, 'q1_proc':'q5_proc'].columns.to_list()
    # question_list = data_2024.loc[:, f'q1_{postpend}':f'q5_{postpend}'].columns.to_list()
    plot_comparison_graph(data_2023, data_2024, postpend, 'unfiltered')

    # for question in question_list:
    #     answer_distribution_actual(data_2024, question)
    #     answer_distribution_actual(data_2023, question)



def print_that_latex():
    # 2024 data
    data_2024 = load_data('csv/resultater24.tsv')
    data_2023 = load_data('csv/resultater23.tsv')
    # print("\n\nGruppe 1 vs Gruppe 2 som ikke har sett animasjonsvideoen")
    # t_test_comparison('proc', data_2024, False)
    #
    # print("\n\nGruppe 1 vs Gruppe 2 som har sett animasjonsvideoen")
    # t_test_comparison('proc', data_2024, True)
    # print_t_test_results(data_2024)
    questions = [*data_2024.loc[:, 'tidseffektivt_proc':'engasjerende_proc'].columns.to_list()]
    questions.extend(data_2024.loc[:, 'tidseffektivt_animert_proc':'engasjerende_animert_proc'].columns.to_list())
    # questions.extend(data_2024.loc[:, 'tidseffektivt_virt':'engasjerende_virt'].columns.to_list())
    # questions.extend(data_2024.loc[:, 'tidseffektivt_animert_virt':'engasjerende_animert_virt'].columns.to_list())
    for question in questions:
        print("\n----------")
        print(question.upper() + ":")
        answer_distribution(data_2024.copy(), question)


def answer_distribution(data_2024, question):
    dist_values = data_2024.loc[:, f'{question}'].value_counts(dropna=True, normalize=True).mul(100).reindex(range(6), fill_value=0).sort_index().round(2).to_list()
    processed_values = data_2024.loc['0':, f'{question}'].dropna()
    mean_value = processed_values.mean()
    std_dev_value = processed_values.std()
    skewness_value = processed_values.skew()

    mean_value = format_number(mean_value)
    std_dev_value = format_number(std_dev_value)
    skewness_value = format_number(skewness_value)

    latex_string = dedent("""\
        Percentage distribution & & & {dist_values[0]} & {dist_values[1]} & {dist_values[2]} & {dist_values[3]} & {dist_values[4]} & {dist_values[5]} \\\\
        Mean & \\multicolumn{{6}}{{l}}{{{mean}}} \\\\
        Standard deviation & \\multicolumn{{6}}{{l}}{{{std_dev}}} \\\\
        Skewness & \\multicolumn{{6}}{{l}}{{{skewness}}} \\\\ \\hline
        """).format(dist_values=dist_values, mean=mean_value, std_dev=std_dev_value, skewness=skewness_value)

    print(latex_string)



def answer_distribution_actual(data, question):
    row_start = data.index[3]
    answer_alternatives = data.loc['answers', f'{question}'].split(',')
    num_alternatives = len(answer_alternatives)
    dist_values = data.loc[row_start:, f'{question}'].value_counts(dropna=True, normalize=True).mul(100).reindex(range(num_alternatives), fill_value=0).sort_index().round(2).to_list()
    processed_values = data.loc[row_start:, f'{question}'].dropna()
    mean_value = processed_values.mean()
    std_dev_value = processed_values.std()
    skewness_value = processed_values.skew()

    # Assuming format_number is a function you've defined to format the numbers for LaTeX
    mean_value = format_number(mean_value)
    std_dev_value = format_number(std_dev_value)
    skewness_value = format_number(skewness_value)

    correct_answer = int(data.loc['correct_answers', f'{question}'])
    dist_values = [dist_values[correct_answer]] + sorted(
        dist_values[:correct_answer] + dist_values[correct_answer + 1:], reverse=True)

    # Creating the bold labels and makecell question alternatives
    bold_labels_list = ['R', 'W1', 'W2', 'W3']
    bold_labels = "&".join([f' \\textbf{{{label}}} &' if idx == 0 else f' \\textbf{{{label}}} ' for idx, label in enumerate(bold_labels_list)])
    makecell_questions = ' & '.join([f'\\makecell{{{alt.replace(" ", "\\\\")}}}' for alt in answer_alternatives])

    # Creating the tabular column alignment string dynamically based on num_alternatives
    column_alignment = 'l' + 'c' * (num_alternatives + 4)
    # Dynamically creating the distribution values part of the LaTeX string
    # an extra & after the first element in dist_values_str
    dist_values_str = ' & '.join(map(str, dist_values[1:num_alternatives]))


    question_text = data.loc['questions', f'{question}']

    # Forming the complete LaTeX string
    latex_string = dedent(f"""\
    {question_text}:& & & {dist_values[0]} && {dist_values_str} \\\\
    """)

    print(latex_string)

def answer_distribution_actual_2(data, question):
    answer_alternatives = data.loc['answers', f'{question}'].split(',')
    num_alternatives = len(answer_alternatives)
    print(num_alternatives)
    dist_values = data.loc['0':, f'{question}'].value_counts(dropna=True, normalize=True).mul(100).reindex(range(num_alternatives), fill_value=0).sort_index().round(2).to_list()
    processed_values = data.loc['0':, f'{question}'].dropna()
    mean_value = processed_values.mean()
    std_dev_value = processed_values.std()
    skewness_value = processed_values.skew()

    mean_value = format_number(mean_value)
    std_dev_value = format_number(std_dev_value)
    skewness_value = format_number(skewness_value)

    # Dynamically creating the distribution values part of the LaTeX string
    dist_values_str = ' & '.join(map(str, dist_values[:num_alternatives]))

    # Forming the complete LaTeX string
    latex_string = dedent(f"""\
            Percentage distribution & & & {dist_values_str} \\\\
            Mean & \\multicolumn{{6}}{{l}}{{{mean_value}}} \\\\
            Standard deviation & \\multicolumn{{6}}{{l}}{{{std_dev_value}}} \\\\
            Skewness & \\multicolumn{{6}}{{l}}{{{skewness_value}}} \\\\ \\hline
            """)

    print(latex_string)

def format_number(value):
    """
    Format a number to two decimal places.
    - For numbers between -1 and 1 (excluding 0), strip the leading zero.
    - Ensure exactly 0 is formatted as '0.00'.
    - Otherwise, format normally to two decimal places.
    """
    value = float(f'{value:.2f}')
    if value == 0:
        return "0.00"
    elif -1 < value < 1:
        return f'{value:.2f}'.lstrip('0')
    else:
        return f'{value:.2f}'


def print_t_test_results(data_2024):
    category = 'virt'
    print("T test comparison for virtual memory questions, not seen animation filtered out")
    t_test_comparison(category, data_2024.copy(), filter_out=True)
    print("T test comparison for virtual memory questions, not seen animation included")
    t_test_comparison(category, data_2024.copy(), filter_out=False)
    category = 'proc'
    print("T test comparison for process questions, not seen animation filtered out")
    t_test_comparison(category, data_2024.copy(), filter_out=True)
    print("T test comparison for process questions, not seen animation included")
    t_test_comparison(category, data_2024.copy(), filter_out=False)


def filter_out_not_seen_lecture(data_2023, results_individual_2023, category):
    return results_individual_2023.loc[
        data_2023.loc[results_individual_2023.index, f'mange_i_snitt_{category}'] != '0']


def filter_out_seen_animation(data_2024, results_individual_2024, category):
    return results_individual_2024.loc[
        data_2024.loc[results_individual_2024.index, f'mange_i_snitt_animert_{category}'] == '0']


def t_test_comparison(category, data_2023, data_2024, filter_out=True):
    results_individual_2024 = calculate_correct_answers(data_2024, f'q1_{category}', f'q5_{category}')
    if filter_out:
        results_individual_2024 = filter_out_not_seen_animation(data_2024, results_individual_2024, category)
    else:
        results_individual_2024 = filter_out_seen_animation(data_2024, results_individual_2024, category)
    # print(results_individual_2024)
    mean_participant_2024_array = calculate_mean(results_individual_2024)
    # one_way_anova_2024 = perform_one_way_anova(results_individual_2024)
    # 2023 data
    results_individual_2023 = calculate_correct_answers(data_2023, f'q1_{category}', f'q5_{category}')
    if filter_out:
        results_individual_2023 = filter_out_not_seen_lecture(data_2023, results_individual_2023, category)
    mean_participant_2023_array = calculate_mean(results_individual_2023)
    # one_way_anova_2023 = perform_one_way_anova(results_individual_2023)
    # check if variance is ratio is less than 4:1
    variance_2024 = calculate_variance(mean_participant_2024_array)
    variance_2023 = calculate_variance(mean_participant_2023_array)
    t_stat, p_value = perform_t_test(mean_participant_2024_array, mean_participant_2023_array)
    print("T-statistic:", t_stat)
    print("P-value:", p_value)

    return results_individual_2023, results_individual_2024


if __name__ == "__main__":
    main()

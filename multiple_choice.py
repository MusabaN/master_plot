from collections import Counter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from utils import adjust_labels


def correct_answers(data, postpend='_proc'):
    correct_answers = data.loc['correct_answers', f'q1{postpend}':f'q5{postpend}']
    candidates_answers = data.loc['0':, f'q1{postpend}':f'q5{postpend}']

    num_correct = [0 for _ in range(6)]
    # iterate over the candidate_answers
    for _, row in candidates_answers.iterrows():
        counter = sum(answer == correct for answer, correct in zip(row, correct_answers))
        num_correct[counter] += 1

    return num_correct

def plot_bar(num_correct):
    sns.set(style="whitegrid")
    sns.barplot(x=[0, 1, 2, 3, 4, 5], y=num_correct, legend=False)
    plt.show()


def bar_graph_general(data, question, title, postpend=''):
    answers = data.loc['0':, f'{question}{postpend}']
    alternatives = data.loc['answers', f'{question}{postpend}'].split(', ')

    answers_lists = answers.apply(lambda x: [int(i) for i in x.split(',') if i.isdigit()])

    # concat all the answers_list into one list as a list comprehension
    all_answers = [answer for answers_list in answers_lists for answer in answers_list]

    frequencies = Counter(all_answers)

    frequencies_df = pd.DataFrame(frequencies.items(), columns=['Choice', 'Frequency'])
    frequencies_df['Choice'] = frequencies_df['Choice'].apply(lambda x: alternatives[x])

    # Set 'Choice' as a categorical variable with the categories ordered as per 'alternatives'
    frequencies_df['Choice'] = pd.Categorical(frequencies_df['Choice'], categories=alternatives, ordered=True)

    # Sort the DataFrame based on this ordered categorical 'Choice'
    frequencies_df = frequencies_df.sort_values('Choice')

    plt.figure(figsize=(14, 8))

    # Create the bar graph with hues
    bar_graph = sns.barplot(data=frequencies_df, x="Choice", y="Frequency", hue="Choice", dodge=False,
                            palette="viridis")

    bar_graph.set_ylabel("Frequency")  # Set the y-axis label
    plt.xticks(rotation=45, ha="right", va="top", rotation_mode="anchor")  # Rotate x-axis labels for better readability
    plt.title(f"{title}")

    # Adjust the layout to make room for the rotated x-axis labels
    plt.tight_layout()

    # Additionally, adjust the bottom margin of the plot to ensure there's enough space for the x-labels
    plt.subplots_adjust(bottom=0.2)  # You may adjust this value as needed
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', axis='y')

    plt.show()


def bar_graph_general_gpt(data, question, title, postpend=''):
    answers = data.loc['0':, f'{question}{postpend}']
    alternatives = data.loc['answers', f'{question}{postpend}'].split(', ')

    # Adjust the alternatives for better readability
    adjusted_alternatives = adjust_labels(alternatives)

    answers_lists = answers.apply(lambda x: [int(i) for i in x.split(',') if i.isdigit()])

    # Concat all the answers_list into one list as a list comprehension
    all_answers = [answer for answers_list in answers_lists for answer in answers_list]

    frequencies = Counter(all_answers)

    frequencies_df = pd.DataFrame(frequencies.items(), columns=['Choice', 'Frequency'])

    # Create a mapping from the original index to the adjusted label
    label_mapping = {index: label for index, label in enumerate(adjusted_alternatives)}

    # Apply the mapping to the 'Choice' column to replace it with the adjusted labels
    frequencies_df['Choice'] = frequencies_df['Choice'].apply(lambda x: label_mapping.get(x, 'Unknown'))

    # Now, set the order of 'Choice' in frequencies_df to match the order of adjusted_alternatives
    frequencies_df['Choice'] = pd.Categorical(frequencies_df['Choice'], categories=adjusted_alternatives, ordered=True)

    # Sort the DataFrame based on the ordered category
    frequencies_df.sort_values('Choice', inplace=True)

    plt.figure(figsize=(14, 8))

    # Create the bar graph with hues
    barplot = sns.barplot(data=frequencies_df, x='Choice', y='Frequency')

    plt.ylabel('Frequency')
    plt.xlabel('\nChoice')
    plt.xticks(rotation=0)  # Set x-axis labels to horizontal
    plt.title(title)

    plt.gca().tick_params(axis='x', which='major', pad=15)

    # Loop over the bars in the barplot and add text with the frequency inside each bar
    for bar in barplot.patches:
        # The text to display is the y-value for this bar
        text = f'{int(bar.get_height())}'

        # Place the text inside the bar, centered
        text_x = bar.get_x() + bar.get_width() / 2
        text_y = bar.get_height() / 2

        barplot.text(text_x, text_y, text,
                     ha='center', va='center', color='white', size=12)

    plt.tight_layout()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', axis='y')

    plt.show()


def compare_bar_graph(last_year, this_year):
    last_year = [(x / sum(last_year)) * 100 for x in last_year]
    this_year = [(x / sum(this_year)) * 100 for x in this_year]
    # Convert lists into a DataFrame
    data = {
        'Score': [0, 1, 2, 3, 4, 5] * 2,  # Scores from 0 to 5, repeated for both years
        'Number of Candidates': last_year + this_year,  # Concatenate the lists
        'Year': ['Last Year'] * 6 + ['This Year'] * 6  # Label each group
    }

    df = pd.DataFrame(data)

    # Create the bar graph
    sns.set(style="whitegrid")  # Setting the seaborn style
    plt.figure(figsize=(10, 6))  # Set the figure size
    barplot = sns.barplot(x='Score', y='Number of Candidates', hue='Year', data=df)  # Create a barplot

    plt.title('Comparison of Candidate Scores from Last Year to This Year')  # Add a title
    plt.xlabel('Score')  # Label the x-axis
    plt.ylabel('Number of Candidates')  # Label the y-axis
    plt.legend(title='Year')  # Add legend
    plt.show()  # Display the plot

def main():
    data_path = 'csv/resultater24.tsv'  # Replace with the correct path to your data file
    data = pd.read_csv(data_path, delimiter='\t', index_col=0)

    virt_24 = correct_answers(data, postpend='_virt')
    proc_24 = correct_answers(data, postpend='_proc')

    data_path = 'csv/resultater23.tsv'
    data = pd.read_csv(data_path, delimiter='\t', index_col=0)
    virt_23 = correct_answers(data, postpend='_virt')
    proc_23 = correct_answers(data, postpend='_proc')
    compare_bar_graph(virt_23.copy(), virt_24.copy())
    compare_bar_graph(proc_23.copy(), proc_24.copy())

    this_year = virt_24.copy()
    last_year = virt_23.copy()
    scores = [0, 1, 2, 3, 4, 5]
    last_year_average = sum(score * count for score, count in zip(scores, last_year)) / sum(last_year)
    this_year_average = sum(score * count for score, count in zip(scores, this_year)) / sum(this_year)

    print(f'2023 average virtual: {last_year_average}')
    print(f'2024 average virtual: {this_year_average}')

    this_year = proc_24.copy()
    last_year = proc_23.copy()
    scores = [0, 1, 2, 3, 4, 5]
    last_year_average = sum(score * count for score, count in zip(scores, last_year)) / sum(last_year)
    this_year_average = sum(score * count for score, count in zip(scores, this_year)) / sum(this_year)

    print(f'2023 average process: {last_year_average}')
    print(f'2024 average process: {this_year_average}')

    # bar_graph_general_gpt(data, 'andre_ressurser', 'Used learning resources for processes', postpend='_virt')
    # bar_graph_general_gpt(data, 'mange_videoer', 'title hehe', postpend='_virt')
    # bar_graph_general_gpt(data, 'mange_videoer', 'title hehe', postpend='_virt')
    # bar_graph_general_gpt(data, 'hyppighet', 'lil_bitch')


if __name__ == "__main__":
    main()

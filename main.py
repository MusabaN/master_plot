from collections import Counter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def insert_line_breaks(label):
    max_len = 5
    # Handling forward slash
    if '/' in label and len(label) > max_len:
        parts = label.split('/')
        # Ensure there are parts to work with and rejoin with a line break
        if len(parts) >= 2:
            return f'{parts[0]} /\n{parts[1]}'
    # Handling spaces
    if ' ' in label and len(label) > max_len:
        parts = label.split(' ')
        # Find the first occurrence where rejoining parts exceeds max_len characters
        for i in range(1, len(parts)):
            if len(' '.join(parts[:i])) > max_len:
                return ' '.join(parts[:i]) + '\n' + ' '.join(parts[i:])
        return label
    return label


# Apply the custom function to each alternative
def adjust_labels(alternatives):
    return [insert_line_breaks(alt) for alt in alternatives]


def correct_answers(data, postpend='_proc'):
    correct_answers = data.loc['correct_answers', f'q1{postpend}':f'q5{postpend}']
    candidates_answers = data.loc['0':, f'q1{postpend}':f'q5{postpend}']

    num_correct = [0 for _ in range(6)]
    # iterate over the candidate_answers
    for _, row in candidates_answers.iterrows():
        counter = sum(answer == correct for answer, correct in zip(row, correct_answers))
        num_correct[counter] += 1

    sns.set(style="whitegrid")
    sns.barplot(x=[0, 1, 2, 3, 4, 5], y=num_correct, palette="Blues_d", hue=[0, 1, 2, 3, 4, 5], legend=False)
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


def main():
    data_path = 'resultater23_v2.tsv'  # Replace with the correct path to your data file
    data = pd.read_csv(data_path, delimiter='\t', index_col=0)

    # correct_answers(data, which_question='virt')
    bar_graph_general_gpt(data, 'andre_ressurser', 'Used learning resources for processes', postpend='_virt')
    bar_graph_general_gpt(data, 'mange_videoer', 'title hehe', postpend='_virt')
    bar_graph_general_gpt(data, 'mange_videoer', 'title hehe', postpend='_virt')
    bar_graph_general_gpt(data, 'hyppighet', 'lil_bitch')


if __name__ == "__main__":
    main()

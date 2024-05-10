from datetime import timedelta
from textwrap import dedent

import numpy as np
import pandas as pd

def load_data(path):
    def seconder(x):
        if '-' in x:
            return np.NAN
        mins, secs = map(float, x.split(':'))
        td = timedelta(minutes=mins, seconds=secs)
        return td.total_seconds()

    data = pd.read_csv(path, delimiter='\t', index_col=0)
    data.loc['0':, 'tid'] = data.loc['0':, 'tid'].apply(lambda x: seconder(x))

    data.loc['0':, 'plattform'] = data.loc['0':, 'plattform'].apply(lambda x: x.split(',') if isinstance(x, str) else x)
    data.loc['0':, 'andre_ressurser_proc'] = data.loc['0':, 'andre_ressurser_proc'].apply(
        lambda x: x.split(',') if isinstance(x, str) else x)
    data.loc['0':, 'andre_ressurser_virt'] = data.loc['0':, 'andre_ressurser_virt'].apply(
        lambda x: x.split(',') if isinstance(x, str) else x)
    # Check if '0' exists in the DataFrame index to avoid errors
    if '0' in data.index:
        columns_to_skip = ['plattform', 'tid', 'andre_ressurser_proc', 'andre_ressurser_virt']
        # Apply the replacement and conversion only from row '0' onwards
        data.loc['correct_answers':, data.columns.difference(columns_to_skip)] = data.loc['correct_answers':,
                                                                                 data.columns.difference(
                                                                                     columns_to_skip)].replace("-",
                                                                                                               np.nan).infer_objects(
            copy=False)
        data.loc['correct_answers':, data.columns.difference(columns_to_skip)] = data.loc['correct_answers':,
                                                                                 data.columns.difference(
                                                                                     columns_to_skip)].apply(
            pd.to_numeric, errors='coerce')
    return data


def average_time(data):
    # Calculate the average time for each category
    avg_time = data.loc['0':, 'tid'].mean()
    return avg_time


def plattform(data):
    # Answer posibilities
    answers = data.loc['answers', 'plattform'].split(', ')
    # count all answers, remember they are in lists value_contes
    exploded = data.loc['0':, 'plattform'].explode().astype(int)
    distribution = exploded.value_counts(normalize=True).mul(100).round(2).sort_index()
    # answers as keys, and counts as values
    value_counts = {answers[i]: distribution[i] for i in range(len(answers))}

    latex_string(answers, distribution, len(answers), exploded.dropna(), data.loc['questions', 'plattform'])


def hyppighet(data):
    # Answer posibilities
    answers = data.loc['answers', 'hyppighet'].split(', ')
    # count all answers, remember they are in lists value_contes
    exploded = data.loc['0':, 'hyppighet']
    distribution = exploded.value_counts(normalize=True).mul(100).round(2).sort_index()
    latex_string(answers, distribution, len(answers), exploded.dropna(), data.loc['questions', 'hyppighet'])


def mange_videoer(data, subsub, ext, include_statistics=False, print_alternatives=False):
    # Answer posibilities
    answers = data.loc['answers', f'mange_videoer{ext}'].split(', ')
    # count all answers, remember they are in lists value_contes
    exploded = data.loc['0':, f'mange_videoer{ext}']
    distribution = exploded.value_counts(normalize=True).mul(100).reindex(range(len(answers)), fill_value=0).round(
        2).sort_index()
    latex_string_v2(answers, distribution, len(answers), exploded.dropna(),
                    data.loc['questions', f'mange_videoer{ext}'], subsub, print_alternatives, include_statistics
                    )


def mange_i_snitt(data, subsub, ext, animated, include_statistics=False, print_alternatives=False):
    col = f'mange_i_snitt{"_animert" if animated else ""}{ext}'
    # Answer posibilities
    answers = data.loc['answers', col].split(', ')
    # count all answers, remember they are in lists value_contes
    exploded = data.loc['0':, col]
    distribution = exploded.value_counts(normalize=True).mul(100).reindex(range(len(exploded)), fill_value=0).round(
        2).sort_index()
    latex_string_v2(answers, distribution, len(answers), exploded.dropna(), data.loc['questions', col], subsub, print_alternatives, include_statistics)


def tidseffektivt(data, subsub, ext, animated, include_statistics=False, print_alternatives=False):
    col = f'tidseffektivt{"_animert" if animated else ""}{ext}'
    # Answer posibilities
    answers = data.loc['answers', col].split(', ')
    # count all answers, remember they are in lists value_contes
    exploded = data.loc['0':, col]
    distribution = exploded.value_counts(normalize=True).mul(100).reindex(range(len(answers)), fill_value=0).round(
        2).sort_index()
    latex_string_v2(answers, distribution, len(answers), exploded.dropna(), data.loc['questions', col], subsub, print_alternatives, include_statistics)


def laeringsutbytte(data, subsub, ext, animated, include_statistics, print_alternatives=False):
    col = f'laeringsutbytte{"_animert" if animated else ""}{ext}'
    # Answer posibilities
    answers = data.loc['answers', col].split(', ')
    # count all answers, remember they are in lists value_contes
    exploded = data.loc['0':, col]
    distribution = exploded.value_counts(normalize=True).mul(100).reindex(range(len(answers)), fill_value=0).round(
        2).sort_index()
    latex_string_v2(answers, distribution, len(answers), exploded.dropna(), data.loc['questions', col], subsub, print_alternatives, include_statistics)


def engasjerende(data, subsub, ext, animated, include_statistics, print_alternatives=False):
    col = f'engasjerende{"_animert" if animated else ""}{ext}'
    # Answer posibilities
    answers = data.loc['answers', col].split(', ')
    # count all answers, remember they are in lists value_contes
    exploded = data.loc['0':, col]
    distribution = exploded.value_counts(normalize=True).mul(100).reindex(range(len(answers)), fill_value=0).round(
        2).sort_index()
    latex_string_v2(answers, distribution, len(answers), exploded.dropna(), data.loc['questions', col], subsub, print_alternatives, include_statistics)


def andre_ressurser(data, ext, subsub, include_statistics, print_alternatives=False):
    col = f'andre_ressurser{ext}'
    # Answer posibilities
    answers = data.loc['answers', col].split(', ')
    # count all answers, remember they are in lists value_contes
    exploded = data.loc['0':, col].explode().replace('-', np.NAN).dropna().astype(int)
    distribution = exploded.value_counts(normalize=True).mul(100).reindex(range(len(answers)), fill_value=0).round(
        2).sort_index()
    latex_string_v2(answers, distribution, len(answers), exploded.dropna(), data.loc['questions', col], subsub, print_alternatives, include_statistics)


def main():
    global include_statistics, print_alternatives
    data24 = load_data('csv/resultater24.tsv')
    data23 = load_data('csv/resultater23.tsv')

    # print("2024 students")
    # plattform(data24)
    # print("2023 students")
    # andre_ressurser(data23)
    for ext in ['_proc', '_virt']:
        mange_videoer(data23, "2023 - group", ext, True, True)
        mange_videoer(data24, "2024 - group", ext, True)
        mange_i_snitt(data23, "2023 - group", ext, False, True, True)
        mange_i_snitt(data24, "2024 - group", ext, False, True, False)
        mange_i_snitt(data24, "2024 - group animated", ext, True, True, False)
        tidseffektivt(data23, "2023 - group", ext, False, True, True)
        tidseffektivt(data24, "2024 - group", ext, False, True, False)
        tidseffektivt(data24, "2024 - group animated", ext, True, True, False)
        laeringsutbytte(data23, "2023 - group", ext, False, True, True)
        laeringsutbytte(data24, "2024 - group", ext, False, True, False)
        laeringsutbytte(data24, "2024 - group animated", ext, True, True, False)
        engasjerende(data23, "2023 - group", ext, False, True, True)
        engasjerende(data24, "2024 - group", ext, False, True, False)
        engasjerende(data24, "2024 - group animated", ext, True, True, False)
        andre_ressurser(data23, ext, "2023 - group", False, True)
        andre_ressurser(data24, ext, "2024 - group", False, False)

    # mange_i_snitt(data24, ext=ext, animated=True)
    # tidseffektivt(data24, ext=ext, animated=True)
    # laeringsutbytte(data24, ext=ext, animated=True)
    # engasjerende(data24, ext=ext, animated=True)
    # andre_ressurser(data24)


def latex_string(answer_alternatives, dist_values, num_alternatives, processed_values, question_text):
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

    mean_value = processed_values.mean()
    std_dev_value = processed_values.std()
    skewness_value = processed_values.skew()
    # Assuming format_number is a function you've defined to format the numbers for LaTeX
    mean_value = format_number(mean_value)
    std_dev_value = format_number(std_dev_value)
    skewness_value = format_number(skewness_value)
    # Creating the bold labels and makecell question alternatives
    bold_labels = ' & '.join([f'\\textbf{{{i}}}' for i in range(num_alternatives)])
    makecell_questions = ' & '.join([f'\\makecell{{{alt.replace(" ", "\\\\")}}}' for alt in answer_alternatives])
    # Creating the tabular column alignment string dynamically based on num_alternatives
    column_alignment = 'l' + 'c' * (num_alternatives + 2)
    # Dynamically creating the distribution values part of the LaTeX string
    dist_values_str = ' & '.join(map(str, dist_values[:num_alternatives]))
    # Forming the complete LaTeX string
    latex_string = dedent(f"""\
    \\begin{{table}}[H]
    \\centering
    \\caption{{Percentage distribution, mean, standard deviation, and skewness for the independent variable of the question \"{question_text}\"}}
    \\begin{{tabular}}{{{column_alignment}}}
    \\hline
     & & & {bold_labels} \\\\ \\cline{{4-{num_alternatives + 3}}}
     & & & {makecell_questions} \\\\ \\hline
    Percentage distribution & & & {dist_values_str} \\\\
    Mean & \\multicolumn{{6}}{{l}}{{{mean_value}}} \\\\
    Standard deviation & \\multicolumn{{6}}{{l}}{{{std_dev_value}}} \\\\
    Skewness & \\multicolumn{{6}}{{l}}{{{skewness_value}}} \\\\ \\hline
    \\end{{tabular}}
    \\end{{table}}
    """)
    print(latex_string)


def latex_string_v2(answer_alternatives, dist_values, num_alternatives, processed_values, question, subsection, print_alternatives2, include_statistics2):
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

    mean_value = processed_values.mean()
    std_dev_value = processed_values.std()
    skewness_value = processed_values.skew()
    # Assuming format_number is a function you've defined to format the numbers for LaTeX
    mean_value = format_number(mean_value)
    std_dev_value = format_number(std_dev_value)
    skewness_value = format_number(skewness_value)
    # Creating the bold labels and makecell question alternatives
    bold_labels = ' & '.join([f'\\textbf{{{i}}}' for i in range(num_alternatives)])
    formatted_alternatives = '\\\\\n'.join([f'{idx}: {alt}' for idx, alt in enumerate(answer_alternatives)])
    if print_alternatives2:
        print(f"\\subsection{{{question}}}")
        print("\\textbf{Alternatives}\\\\")
        print(formatted_alternatives)
    print(f"\\subsubsection{{{subsection}}}")
    # Creating the tabular column alignment string dynamically based on num_alternatives
    column_alignment = 'l' + 'c' * (num_alternatives + 2)
    # Dynamically creating the distribution values part of the LaTeX string
    dist_values_str = ' & '.join(map(str, dist_values[:num_alternatives]))
    statistic_lines = ""
    statistic_lines = f"""\
    Mean & \\multicolumn{{6}}{{l}}{{{mean_value}}} \\\\
    Standard deviation & \\multicolumn{{6}}{{l}}{{{std_dev_value}}} \\\\
    Skewness & \\multicolumn{{6}}{{l}}{{{skewness_value}}} \\\\ \\hline
    """
    if not include_statistics2:
        statistic_lines = ""
    # Forming the complete LaTeX string
    latex_string = f"""\
    \\begin{{table}}[H]
    \\centering
    \\begin{{tabular}}{{{column_alignment}}}
    
    \\hline
     & & & {bold_labels} \\\\ \\cline{{4-{num_alternatives + 3}}}
    Percentage distribution & & & {dist_values_str} \\\\
{statistic_lines}
    \\end{{tabular}}
    \\end{{table}}
    """
    print(dedent(latex_string))


if __name__ == "__main__":
    main()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_and_normalize_data(csv_path):
    """Load data from CSV and normalize the percentages."""
    df = pd.read_csv(csv_path)

    # Normalize the values to percentages (if not already done before saving to CSV)
    for year in ['2023', '2024', '2024 Animated']:
        df[year] = (df[year] / df[year].sum()) * 100

    # Reshape data for plotting
    return df.melt(id_vars=['Question', 'Alternative'], var_name='Year', value_name='Percentage')


def plot_bar_graph(df_melted, category):
    """Plot bar graphs for each question."""
    sns.set(style='whitegrid')
    questions = df_melted['Question'].unique()
    for question in questions:
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Alternative', y='Percentage', hue='Year', data=df_melted[df_melted['Question'] == question])
        plt.title(f'Comparison of {question} Across Years')
        plt.ylabel('Percentage (%)')
        plt.xlabel('Alternatives')
        plt.legend(title='Year')
        plt.savefig('./plots/' + question + '_' + category + '.png')


def main():
    category = ''
    if category == 'proc':
        csv_path = './csv/mcqs_processes.csv'  # Replace with your actual CSV file path
        df_melted = load_and_normalize_data(csv_path)
        plot_bar_graph(df_melted, "processes")
    else:
        csv_path = './csv/mcqs_virtual.csv'
        df_melted = load_and_normalize_data(csv_path)
        plot_bar_graph(df_melted, "virtual")


if __name__ == "__main__":
    main()

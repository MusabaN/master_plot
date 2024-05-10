import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_bar_graph(csv_path):
    # Load data from CSV
    df = pd.read_csv(csv_path)

    # Normalize the values to percentages (if not already done before saving to CSV)
    for year in ['2023', '2024', '2024 Animated']:
        df[year] = (df[year] / df[year].sum()) * 100

    # Reshape data for plotting
    df_melted = df.melt(id_vars=['Question', 'Alternative'], var_name='Year', value_name='Percentage')

    # Setup the style
    sns.set(style='whitegrid')

    # Plotting each question in a separate plot
    questions = df['Question'].unique()
    for question in questions:
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Alternative', y='Percentage', hue='Year', data=df_melted[df_melted['Question'] == question])
        plt.title(f'Comparison of {question} Across Years')
        plt.ylabel('Percentage (%)')
        plt.xlabel('Alternatives')
        plt.legend(title='Year')
        plt.show()


def main():
    csv_path = './csv/mcqs_processes.csv'  # Replace with your actual CSV file path
    plot_bar_graph(csv_path)


if __name__ == "__main__":
    main()

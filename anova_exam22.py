import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f_oneway
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def fetch_exam_data():
    """
    Fetches the exam data from the exam_results_2022.tsv file.

    Returns:
    - DataFrame: A pandas DataFrame containing the exam data.

    Data description:
    - Columns contain the participant IDs and their score in the different categories.
    - Rows contain the category names and participants scores in those categories.
    """
    # load the data
    data = pd.read_csv('csv/exam_results_2022.tsv', delimiter='\t', index_col=0, decimal=',')

    # Convert all columns to float, coercing errors to NaN
    data = data.astype(float)
    # Convert 0s to NaNs
    data = data.replace(0, np.NAN)

    return data


def fill_with_mean(series):
    """
    Takes a pandas Series, calculates the mean of non-zero elements,
    and returns the Series with zeros replaced by this mean.
    """
    # print(series)
    mean = series.mean(skipna=True)
    return series.replace(np.NAN, mean)


def main():
    data = fetch_exam_data()
    # for each category, calculate the mean score excluding zeros, fill zeros in each category with the mean
    data = data.iloc[:data.index.get_loc('sum'), :].apply(fill_with_mean, axis=1)

    # perform the ANOVA test
    groups = [data.loc[category].values for category in data.index]  # Extract groups as arrays

    # Perform ANOVA
    f_stat, p_value = f_oneway(*groups)
    print(f'F-statistic: {f_stat:.2f}, p-value: {p_value:.4f}')

    # If ANOVA shows significant differences, proceed with Tukey's HSD
    if p_value < 0.05:
        # Flatten the list of arrays into a single array for the Tukey test
        all_values = np.concatenate(groups)
        # Create a corresponding array of group labels
        labels = np.array([label for i, row in enumerate(data.index) for label in [row] * len(data.loc[row])])
        print(len(labels))

        # Perform Tukey's HSD
        tukey_results = pairwise_tukeyhsd(all_values, labels, alpha=0.05)
        print(tukey_results)

        # To plot the results
        tukey_results.plot_simultaneous()
        plt.show()


    else:
        print('Fail to reject the null hypothesis')


if __name__ == "__main__":
    main()

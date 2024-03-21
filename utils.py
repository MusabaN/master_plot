import seaborn as sns
import matplotlib.pyplot as plt


def plot_bargraph(data, x, y, hue=None, title='', xlabel='', ylabel='', plot_type='bar', orientation='v', figsize=(10, 6)):
    plt.figure(figsize=figsize)
    if plot_type == 'bar':
        if orientation == 'v':
            sns.barplot(x=x, y=y, hue=hue, data=data)
        else:
            sns.barplot(x=y, y=x, hue=hue, data=data, orient='h')
    # Add other plot types as elif conditions here

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if hue:
        plt.legend(title=hue)
    plt.tight_layout()
    plt.show()


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


def plot_comparison_bargraph(data, title, save_name):
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 8))
    bar_graph = sns.barplot(data=data, palette="viridis")
    bar_graph.set_ylabel("Average points")
    plt.title(f"{title}")
    plt.savefig(f'./plots/{save_name}.png')

def plot_bargraph(ylabel, title, save_name, x_labels, values, values2=None):
    x_labels = adjust_labels(x_labels)
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 8))
    bar_graph = sns.barplot(x=x_labels, y=values)
    bar_graph.set_ylabel(f"{ylabel}")
    start = int(min(values)) - 10
    end = int(max(values)) + 10
    plt.ylim(start, end)
    plt.title(f"{title}")
    plt.savefig(f'./plots/{save_name}.png')

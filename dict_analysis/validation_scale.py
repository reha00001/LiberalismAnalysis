from dict import liberalism_dict
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from liberalness_scale import calculate_frequencies, logit_scaling


def process_folder_validation(folder_name):
    data_dir = Path.cwd() / folder_name
    conf_intervals = []
    file_info = []

    for file_path in data_dir.glob('*.csv'):
        df = pd.read_csv(file_path)
        df = df.dropna()
        df = calculate_frequencies(df, 'comment')
        df = logit_scaling(df)

        # Store confidence intervals with subreddit information
        middle_point = (df.iloc[0]['conf_lower'] + df.iloc[0]['conf_upper']) / 2
        conf_intervals.append((middle_point, df.iloc[0]['conf_lower'], df.iloc[0]['conf_upper']))
        file_info.append((df.iloc[0]['subreddit'], file_path.name))

        file_info_sorted = [x for _, x in sorted(zip([ci[0] for ci in conf_intervals], file_info), reverse=True)]
        conf_intervals_sorted = sorted(conf_intervals, key=lambda x: x[0], reverse=True)

    return conf_intervals_sorted, file_info_sorted

def plot_reddit_validation(folder_name):
    co, fi = process_folder_validation(folder_name)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, len(fi) * 0.7))  # Adjust figsize as needed

    y_pos = np.arange(len(fi))
    for i, (middle_point, conf_lower, conf_upper) in enumerate(co):
        ax.plot([conf_lower, conf_upper], [i, i], color='blue', linewidth=2)  # Use a consistent color for intervals
        ax.plot(middle_point, i, marker='o', color='blue', markersize=8)  # Point in the middle

    ax.axvline(x=0, color='black', linestyle='--')  # Vertical line at x=0
    ax.set_yticks(y_pos)
    ax.set_yticklabels([info[0] for info in fi], fontsize=8)  # Adjust fontsize here
    ax.invert_yaxis()  # Labels read top-to-bottom
    ax.set_xlabel('Confidence Intervals')
    ax.set_title('Reddit Comments Analysis')

    # Add legend annotation
    ax.annotate('Illiberal', xy=(0, -0.2), xycoords='axes fraction', ha='center', va='center', fontsize=12)
    ax.annotate('Liberal', xy=(1, -0.2), xycoords='axes fraction', ha='center', va='center', fontsize=12)

    plt.tight_layout()  # Adjust layout

    plt.show()
from dict import liberalism_dict
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calculate_frequencies(df, row_name):
    illiberal_counts = []
    liberal_counts = []

    for index, row in df.iterrows():
        illiberal_count = 0
        liberal_count = 0
        text = row[row_name]

        # Counting illiberal terms
        for category in liberalism_dict['illiberalism']:
            terms = liberalism_dict['illiberalism'][category]
            for term in terms:
                if text is None or (isinstance(text, float)):
                    continue
                if term in text:
                    illiberal_count += 1

        # Counting liberal terms
        for category in liberalism_dict['liberalism']:
            terms = liberalism_dict['liberalism'][category]
            for term in terms:
                if term in text:
                    liberal_count += 1

        illiberal_counts.append(illiberal_count)
        liberal_counts.append(liberal_count)

    df['Illiberal Count'] = sum(illiberal_counts)
    df['Liberal Count'] = sum(liberal_counts)
    return df


def logit_scaling(df):
    a = 0.5  # Symmetrical invariant Jeffreys prior
    df['I'] = df['Illiberal Count']
    df['L'] = df['Liberal Count']
    df['mu'] = np.log((df['I'] + a) / (df['L'] + a))
    df['sigma_sq'] = (1 / (df['I'] + a)) + (1 / (df['L'] + a))
    df['theta'] = df['mu']
    df['conf_lower'] = -(df['theta'] - 1.96 * np.sqrt(df['sigma_sq']))
    df['conf_upper'] = -(df['theta'] + 1.96 * np.sqrt(df['sigma_sq']))
    return df


def process_folder(folder_name):
    data_dir = Path.cwd() / folder_name
    file_info = []
    conf_intervals = []

    for file_path in data_dir.glob('*.csv'):
        df = pd.read_csv(file_path)
        df = calculate_frequencies(df, 'Speech Content')
        df = logit_scaling(df)

        # Extract file information
        country_speaker = f"{df['Country'].iloc[0]} - {df['Speaker'].iloc[0]}"
        color = df['Color'].iloc[0]  # Green or Red ; Democracy or Autocracy
        file_info.append((country_speaker, color))  # Store tuple of (country_speaker, color)

        # Store confidence intervals
        middle_point = (df.iloc[0]['conf_lower'] + df.iloc[0]['conf_upper']) / 2
        conf_intervals.append((middle_point, df.iloc[0]['conf_lower'], df.iloc[0]['conf_upper'], color))

    # Sort files based on middle point of confidence intervals
    file_info_sorted = [x for _, x in sorted(zip([ci[0] for ci in conf_intervals], file_info), reverse=True)]
    conf_intervals_sorted = sorted(conf_intervals, key=lambda x: x[0], reverse=True)

    # Plotting
    fig, ax = plt.subplots(figsize=(20, len(file_info_sorted) * 0.7))  # Adjust figsize as needed

    y_pos = np.arange(len(file_info_sorted))
    for i, (middle_point, conf_lower, conf_upper, color) in enumerate(conf_intervals_sorted):
        ax.plot([conf_lower, conf_upper], [i, i], color=color, linewidth=2)  # Use color from conf_intervals
        ax.plot(middle_point, i, marker='o', color=color, markersize=8)  # Point in the middle

    ax.axvline(x=0, color='black', linestyle='--')  # Vertical line at x=0
    ax.set_yticks(y_pos)
    ax.set_yticklabels([info[0] for info in file_info_sorted], fontsize=8)  # Adjust fontsize here
    ax.invert_yaxis()  # Labels read top-to-bottom
    ax.set_xlabel('Confidence Intervals')
    ax.text(0.5, -0.1, 'Green = Democracy ; Red = Autocracy', ha='center', va='center', transform=ax.transAxes,
            fontsize=10)
    ax.set_title('Dictionary Analysis')

    # Add legend annotation
    ax.annotate('Illiberal', xy=(0, -0.1), xycoords='axes fraction', ha='center', va='center', fontsize=12)
    ax.annotate('Liberal', xy=(1, -0.1), xycoords='axes fraction', ha='center', va='center', fontsize=12)

    plt.tight_layout()  # Adjust layout

    plt.show()

    # Validation 1 : Criterion Validity
    dem_countries = []
    auto_countries = []

    for i in conf_intervals_sorted:
        if i[3] == 'green':
            dem_countries.append(i)
        if i[3] == 'red':
            auto_countries.append(i)

    # Validation plot
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    dem_values = [i[0] for i in dem_countries]
    dem_values = dem_values[:-1]
    auto_values = [i[0] for i in auto_countries]

    bplot = ax2.boxplot([dem_values, auto_values],
                        positions=[2, 1],
                        vert=False,
                        patch_artist=True,
                        whis=[0, 100],
                        medianprops=dict(color='black', linewidth=1),
                        whiskerprops=dict(color='black', linewidth=1)
                        )

    box_colors = ['green', 'red']
    for patch, color in zip(bplot['boxes'], box_colors):
        patch.set_facecolor(color)

    ax2.set_xlabel("Liberal vs Illiberal Rhetoric")
    ax2.set_yticklabels(['Democracy', 'Autocracy'])
    ax2.set_title('Criterion Validity')

    plt.show()



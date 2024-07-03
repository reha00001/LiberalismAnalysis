from validation_scale import plot_reddit_validation
from liberalness_scale import process_folder

if __name__ == '__main__':

    # Do dict analysis and criterion validation, pass folder name as argument
    process_folder('preprocessed_speeches')

    # Do reddit comments validation, pass folder name as argument
    plot_reddit_validation('reddit_comments')


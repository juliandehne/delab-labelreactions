import sys

import inquirer
import pandas as pd

decision_tree = {
    'after_text': {
        'question': "Is the after_text_reaction a positive horizon (p),"
                    " a negative horizon (n), emotional reaction(e) or an conclusion or metacommunication (c)?",
        'options': ['p', 'n', "e", "c"],
        'next': {
            'p': {
                'question': "Choose an option for 'positive horizon': "
                            "elaboration (e), differentiation (dif), validation (v) or ratification (r):",
                'options': ["e", "dif", "v", "r"],
            },
            'n': {
                'question': "Choose an option for 'negative horizon': antithesis (a), opposition (o), divergence (div)",
                'options': ["a", "o", "div"],
            },
            'e': {
                'question': "Choose an option for 'emotional reaction': positive (pos), negative (neg)",
                'options': ["pos", "neg"],
            },
            'c': {
                'question': "Choose an option for 'conclusion':"
                            " positive evaluation (pe), synthesis (s), topic chance (tc),"
                            " formal synthesis (fs), reject topic (rt), meta communication (m) ",
                'options': ["pe", "tc", "fs", "rt", "s", "m"],
            },

        }
    },
    'aafter_text': {
        'question': "Is the aafter_text_reaction a positive horizon,"
                    " a negative horizon, emotional reaction or an conclusion?",
        'options': ['p', 'n', "e", "c"],
        'next': {
            'p': {
                'question': "Choose an option for 'positive horizon': "
                            "elaboration (e), differentiation (dif), validation (v) or ratification (r):",
                'options': ["e", "dif", "v", "r"],
            },
            'n': {
                'question': "Choose an option for 'negative horizon': antithesis (a), opposition (o), divergence (div)",
                'options': ["a", "o", "div"],
            },
            'e': {
                'question': "Choose an option for 'emotional reaction': positive (pos), negative (neg)",
                'options': ["pos", "neg"],
            },
            'c': {
                'question': "Choose an option for 'conclusion':"
                            " positive evaluation (pe), synthesis (s), topic chance (tc),"
                            " formal synthesis (fs), reject topic (rt), meta communication (m) ",
                'options': ["pe", "tc", "fs", "rt", "s", "m"],
            },

        }
    }
}


def ask_question(question, choices):
    questions = [
        inquirer.List('response',
                      message=question,
                      choices=choices,
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers['response']


def label_based_on_tree(tree, label_col):
    # Ask the initial question
    response = ask_question(tree['question'], tree['options'])

    # Navigate through the tree based on the answer
    if 'next' in tree and response in tree['next']:
        second_response = ask_question(tree['next'][response]['question'], tree['next'][response]['options'])
        return f"{response} -> {second_response}"
    return response


def main(filepath):
    # Load the xlsx file using pandas
    df = pd.read_excel(filepath)

    # Pre-define label columns as 'object' (string) data type if they don't exist
    if 'after_text_label' not in df.columns:
        df['after_text_label'] = ''
    if 'aafter_text_label' not in df.columns:
        df['aafter_text_label'] = ''

    try:
        # Iterate over rows in the DataFrame
        for index, row in df.iterrows():

            # Check if the current row has been labeled previously
            if not pd.isna(row['after_text_label']) and not pd.isna(row['aafter_text_label']):
                continue  # Skip this row if it's already labeled

            # Display the columns by name
            print("m_text:", row['m_text'])
            print("after_text:", row['after_text'])

            # Label after_text
            label_after_text = label_based_on_tree(decision_tree['after_text'], 'after_text')
            df.at[index, 'after_text_label'] = label_after_text
            # print("Label for after_text:", label_after_text)

            # Display the columns by name
            print("m_text:", row['m_text'])
            print("after_text:", row['after_text'])
            print("aafter_text:", row['aafter_text'])

            # Label aafter_text
            label_aafter_text = label_based_on_tree(decision_tree['aafter_text'], 'aafter_text')
            df.at[index, 'aafter_text_label'] = label_aafter_text
            # print("Label for aafter_text:", label_aafter_text)

    except KeyboardInterrupt:  # Catch a keyboard interrupt (Ctrl + C)
        print("\nProcess interrupted by user. Saving current progress...")

    finally:  # This block ensures the data is saved regardless of how the try block exits
        # Save the updated DataFrame
        df.to_excel(filepath, index=False)
        print("Progress saved to:", filepath)

    # Save the updated DataFrame
    df.to_excel(filepath, index=False)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the xlsx file as the first argument.")
        sys.exit(1)
    filepath = sys.argv[1]
    main(filepath)

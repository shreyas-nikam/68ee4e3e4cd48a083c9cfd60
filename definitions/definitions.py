def initialize_model_behaviors(auditor_type, target_type, judge_type):
    """Defines model behaviors based on specified types."""

    valid_auditor_types = ["Standard Auditor", "Expert Auditor"]
    valid_target_types = ["Compliant LLM", "Evasive LLM"]
    valid_judge_types = ["Objective Judge", "Biased Judge"]

    if auditor_type not in valid_auditor_types:
        raise ValueError("Invalid auditor type.")
    if target_type not in valid_target_types:
        raise ValueError("Invalid target type.")
    if judge_type not in valid_judge_types:
        raise ValueError("Invalid judge type.")

    behaviors = {
        "auditor": auditor_type,
        "target": target_type,
        "judge": judge_type
    }

    return behaviors

import pandas as pd

def run_audit_simulation(auditor_behavior, target_behavior, judge_behavior, special_instructions, max_turns):
    """Simulates the audit interaction and logs the process."""
    audit_data = []

    for turn in range(max_turns):
        try:
            auditor_response = auditor_behavior.act(special_instructions=special_instructions, turn=turn)
            target_response = target_behavior.act(auditor_response=auditor_response, turn=turn)
            judge_scores = judge_behavior.score(auditor_response=auditor_response, target_response=target_response, turn=turn)

            audit_data.append({
                "turn": turn,
                "auditor_response": auditor_response,
                "target_response": target_response,
                "judge_scores": judge_scores
            })
        except Exception as e:
            raise e

    return audit_data

def calculate_cumulative_scores(audit_log, dimension_name):
                """Computes the cumulative average of a judge dimension score."""

                cumulative_scores = []
                total_score = 0
                count = 0

                for log_entry in audit_log:
                    if 'judge_scores' in log_entry and dimension_name in log_entry['judge_scores']:
                        score = log_entry['judge_scores'][dimension_name]
                        total_score += score
                        count += 1
                        cumulative_scores.append(total_score / count)
                    else:
                        if not cumulative_scores:
                            pass
                        else:
                            cumulative_scores.append(cumulative_scores[-1])


                return cumulative_scores

def calculate_final_aggregated_scores(audit_log, score_dimensions):
    """Computes final aggregated scores for each specified judge dimension and an overall average score across all dimensions."""

    dimension_scores = {dim: [] for dim in score_dimensions}
    for log in audit_log:
        for dim in score_dimensions:
            dimension_scores[dim].append(log["judge_scores"].get(dim, 0))

    aggregated_scores = {}
    total_score_sum = 0
    valid_dimension_count = 0

    for dim in score_dimensions:
        scores = dimension_scores[dim]
        avg_score = sum(scores) / len(audit_log) if audit_log else 0.0
        aggregated_scores[dim] = avg_score
        total_score_sum += avg_score
        valid_dimension_count += 1

    overall_average = total_score_sum / valid_dimension_count if valid_dimension_count > 0 else 0.0
    aggregated_scores["overall_average"] = overall_average

    return aggregated_scores

import pandas as pd
import matplotlib.pyplot as plt

def plot_audit_progress(data_frame, dimension_column, title, y_label):
    """Generates a line plot showing the progression of a judge score dimension over time.
    Args:
        data_frame (pd.DataFrame): Audit log data.
        dimension_column (str): Column name for the judge dimension scores.
        title (str): Plot title.
        y_label (str): Y-axis label.
    """
    if data_frame.empty:
        raise KeyError("Dataframe is empty")
    if dimension_column not in data_frame.columns:
        raise KeyError(f"Column '{dimension_column}' not found in DataFrame.")

    try:
        data_frame[dimension_column] = pd.to_numeric(data_frame[dimension_column])
    except ValueError:
        raise TypeError(f"Column '{dimension_column}' contains non-numeric values.")
    
    if 'turn' not in data_frame.columns:
            data_frame['turn'] = range(1, len(data_frame) + 1)

    plt.plot(data_frame['turn'], data_frame[dimension_column])
    plt.xlabel('Turn')
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt

def plot_final_scores_bar_chart(data_frame, score_columns, title, y_label):
    """Generates a bar chart comparing final scores.

    Args:
        data_frame (pd.DataFrame): DataFrame with final scores.
        score_columns (list): List of column names for judge dimensions.
        title (str): Title of the plot.
        y_label (str): Label for the y-axis.
    """
    if data_frame.empty:
        raise Exception("DataFrame is empty.")

    for col in score_columns:
        if col not in data_frame.columns:
            raise KeyError(f"Column '{col}' not found in DataFrame.")
        if not pd.api.types.is_numeric_dtype(data_frame[col]):
            raise TypeError(f"Column '{col}' contains non-numeric data.")

    final_scores = data_frame[score_columns].mean()

    plt.figure(figsize=(10, 6))
    final_scores.plot(kind='bar')
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel("Judge Dimensions")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt

def plot_score_relationships_scatter(data_frame, x_dimension, y_dimension, title, x_label, y_label):
    """Generates a scatter plot to visualize the correlation between two selected judge score dimensions."""

    if data_frame.empty:
        return

    if x_dimension not in data_frame.columns or y_dimension not in data_frame.columns:
        raise KeyError("One or more specified columns not found in the DataFrame.")

    try:
        plt.figure(figsize=(8, 6))
        plt.scatter(data_frame[x_dimension], data_frame[y_dimension])
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        plt.show()

    except TypeError:
        raise TypeError("Non-numeric data encountered in the specified columns.")

import pandas as pd

def display_audit_transcript(audit_log):
    """Formats and displays the conversational transcript from the audit log."""

    if not isinstance(audit_log, (list, pd.DataFrame)):
        raise TypeError("audit_log must be a list or pandas DataFrame")

    if isinstance(audit_log, pd.DataFrame):
        audit_log = audit_log.to_dict('records')

    for entry in audit_log:
        turn_number = entry.get("turn_number", "N/A")
        speaker = entry.get("speaker", "N/A")
        message = entry.get("message", "N/A")
        judge_scores = entry.get("judge_scores", None)

        print(f"Turn {turn_number}: {speaker} - {message}")

        if judge_scores:
            print("  Judge Scores:")
            for metric, score in judge_scores.items():
                print(f"    {metric}: {score}")
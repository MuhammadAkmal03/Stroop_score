import pandas as pd
import os


# SCORE CALCULATION

def calculate_scores(block):

    if len(block) == 0:

        return {
            "Neutral": None,
            "Congruent": None,
            "Incongruent": None,
            "IF": None,
            "Facilitation": None
        }

    mean_rt = block.groupby(
        "condition"
    )["rt"].mean()

    neutral = mean_rt.get(
        "Neutral",
        None
    )

    congruent = mean_rt.get(
        "Congruent",
        None
    )

    incongruent = mean_rt.get(
        "Incongruent",
        None
    )

    interference = None
    facilitation = None

    if (
        pd.notna(incongruent)
        and pd.notna(neutral)
    ):
        interference = (
            incongruent - neutral
        )

    if (
        pd.notna(neutral)
        and pd.notna(congruent)
    ):
        facilitation = (
            neutral - congruent
        )

    return {

        "Neutral": neutral,
        "Congruent": congruent,
        "Incongruent": incongruent,
        "IF": interference,
        "Facilitation": facilitation
    }


# CLEAN DATA

def clean_block(data, correct_only=True):

    data = data.copy()

    data["condition"] = (
        data["condition"]
        .astype(str)
        .str.strip()
        .str.capitalize()
    )

    data["corr"] = pd.to_numeric(
        data["corr"],
        errors="coerce"
    )

    data["rt"] = pd.to_numeric(
        data["rt"],
        errors="coerce"
    )

    valid_conditions = [
        "Neutral",
        "Congruent",
        "Incongruent"
    ]

    data = data[
        data["condition"].isin(valid_conditions)
    ]

    data = data.dropna(
        subset=["condition", "rt"]
    )

    if correct_only:
        data = data[
            data["corr"] == 1
        ]

    return data


# PROCESS ONE FILE

def process_single_file(
    file,
    correct_only=True):

    df = pd.read_csv(file)
    
    total_trials = 0
    correct_trials = 0

    high_total_trials = 0
    high_correct_trials = 0

    low_total_trials = 0
    low_correct_trials = 0

    # PARTICIPANT NAME

    participant = "Unknown"

    if isinstance(file, str):

        filename = os.path.basename(file)

    elif hasattr(file, "name"):

        filename = os.path.basename(file.name)

    else:

        filename = "Unknown.csv"

    participant = filename.replace(".csv", "")

    if "_STROOP" in participant:

        participant = participant.split("_STROOP")[0]

    # DETECT BLOCKS

    has_high = (
        "key_resp.rt" in df.columns
        and "key_resp.corr" in df.columns
    )

    has_low = (
        "key_resp_10.rt" in df.columns
        and "key_resp_10.corr" in df.columns
    )

    high_scores = {
        "Neutral": None,
        "Congruent": None,
        "Incongruent": None,
        "IF": None,
        "Facilitation": None
    }

    low_scores = {
        "Neutral": None,
        "Congruent": None,
        "Incongruent": None,
        "IF": None,
        "Facilitation": None
    }

    # LOW ONLY

    if has_low and not has_high:

        low_data = df[
            [
                "condition",
                "key_resp_10.corr",
                "key_resp_10.rt"
            ]
        ].copy()

        valid_conditions = [
            "Neutral",
            "Congruent",
            "Incongruent"
        ]

        low_acc = low_data[
            low_data["condition"]
            .astype(str)
            .str.strip()
            .str.capitalize()
            .isin(valid_conditions)
        ].copy()

        low_acc["key_resp_10.corr"] = pd.to_numeric(
            low_acc["key_resp_10.corr"],
            errors="coerce"
        )

        low_acc = low_acc.dropna(
            subset=["key_resp_10.corr"]
        )

        low_total_trials = len(low_acc)

        low_correct_trials = (
            low_acc["key_resp_10.corr"] == 1
        ).sum()
        

        total_trials += len(low_acc)

        correct_trials += (
            low_acc["key_resp_10.corr"] == 1
        ).sum()

        low_data.columns = [
            "condition",
            "corr",
            "rt"
        ]

        low_data = clean_block(
            low_data,correct_only
        )

        low_scores = calculate_scores(
            low_data
        )

    # HIGH + LOW

    elif has_high and has_low:

        high_data = df[
            [
                "condition",
                "key_resp.corr",
                "key_resp.rt"
            ]
        ].copy()

        valid_conditions = [
            "Neutral",
            "Congruent",
            "Incongruent"
        ]

        high_acc = high_data[
            high_data["condition"]
            .astype(str)
            .str.strip()
            .str.capitalize()
            .isin(valid_conditions)
        ].copy()

        high_acc["key_resp.corr"] = pd.to_numeric(
            high_acc["key_resp.corr"],
            errors="coerce"
        )

        high_acc = high_acc.dropna(
            subset=["key_resp.corr"]
        )

        high_total_trials = len(high_acc)

        high_correct_trials = (
            high_acc["key_resp.corr"] == 1
        ).sum()

        total_trials += len(high_acc)

        correct_trials += (
            high_acc["key_resp.corr"] == 1
        ).sum()

        high_data.columns = [
            "condition",
            "corr",
            "rt"
        ]

        high_data = clean_block(
            high_data,correct_only
        )

        low_data = df[
            [
                "condition",
                "key_resp_10.corr",
                "key_resp_10.rt"
            ]
        ].copy()
        
        valid_conditions = [
            "Neutral",
            "Congruent",
            "Incongruent"
        ]

        low_acc = low_data[
            low_data["condition"]
            .astype(str)
            .str.strip()
            .str.capitalize()
            .isin(valid_conditions)
        ].copy()

        low_acc["key_resp_10.corr"] = pd.to_numeric(
            low_acc["key_resp_10.corr"],
            errors="coerce"
        )

        low_acc = low_acc.dropna(
            subset=["key_resp_10.corr"]
        )

        low_total_trials = len(low_acc)

        low_correct_trials = (
            low_acc["key_resp_10.corr"] == 1
        ).sum()

        total_trials += len(low_acc)

        correct_trials += (
            low_acc["key_resp_10.corr"] == 1
        ).sum()

        low_data.columns = [
            "condition",
            "corr",
            "rt"
        ]

        low_data = clean_block(
            low_data,correct_only
        )

        # Detect which block is low
        low_percentage = (
            (
                high_data["condition"]
                == "Neutral"
            ).mean()
            * 100
        ) if len(high_data) else 0

        if low_percentage >= 70:

            # first block is LOW
            low_scores = calculate_scores(
                high_data
            )

            high_scores = calculate_scores(
                low_data
            )

            low_total_trials, high_total_trials = (
                high_total_trials,
                low_total_trials
            )

            low_correct_trials, high_correct_trials = (
                high_correct_trials,
                low_correct_trials
            )



        else:

            # first block is HIGH
            high_scores = calculate_scores(
                high_data
            )

            low_scores = calculate_scores(
                low_data
            )

    else:

        raise Exception(
            "Required columns missing"
        )

    # OUTPUT
    
    accuracy = None
    high_accuracy = None
    low_accuracy = None

    if total_trials > 0:

        accuracy = round(
            (correct_trials / total_trials) * 100,
            2
        )

    if high_total_trials > 0:

        high_accuracy = round(
            (high_correct_trials / high_total_trials) * 100,
            2
        )

    if low_total_trials > 0:

        low_accuracy = round(
            (low_correct_trials / low_total_trials) * 100,
            2
        )

    return {

        "Participant":
            participant,
        
        "Overall_Accuracy (%)":
            accuracy,

        "33N_Accuracy (%)":
            high_accuracy,

        "75N_Accuracy (%)":
            low_accuracy,

        "33N_Neutral_Mean":
            high_scores["Neutral"],

        "33N_Incongruent_Mean":
            high_scores["Incongruent"],

        "33N_Congruent_Mean":
            high_scores["Congruent"],

        "33N_IF":
            high_scores["IF"],

        "33N_Facilitation":
            high_scores["Facilitation"],

        "75N_Neutral_Mean":
            low_scores["Neutral"],

        "75N_Incongruent_Mean":
            low_scores["Incongruent"],

        "75N_Congruent_Mean":
            low_scores["Congruent"],

        "75N_IF":
            low_scores["IF"],

        "75N_Facilitation":
            low_scores["Facilitation"]
    }


# PROCESS MULTIPLE FILES

def process_multiple_files(
    files,
    correct_only=True):

    results = []

    for file in files:

        try:

            result = process_single_file(
            file,correct_only)

            results.append(
                result
            )

        except Exception as e:

            print(
                f"Error processing {file}"
            )

            print(e)

    return pd.DataFrame(
        results
    )
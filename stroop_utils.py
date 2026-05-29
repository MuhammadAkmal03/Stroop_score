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

def clean_block(data):

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
        data["condition"].isin(
            valid_conditions
        )
    ]

    data = data.dropna(
        subset=["condition", "corr", "rt"]
    )

    # ONLY CORRECT RESPONSES
    data = data[
        data["corr"] == 1
    ]

    return data


# PROCESS ONE FILE

def process_single_file(file):

    df = pd.read_csv(file)

    # PARTICIPANT NAME

    participant = "Unknown"

    if isinstance(file, str):

        participant = os.path.basename(
            os.path.dirname(file)
        )

    elif hasattr(file, "name"):

        participant = (
            os.path.basename(
                file.name
            )
            .replace(".csv", "")
            .split("_STROOP")[0]
        )

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

        low_data.columns = [
            "condition",
            "corr",
            "rt"
        ]

        low_data = clean_block(
            low_data
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

        high_data.columns = [
            "condition",
            "corr",
            "rt"
        ]

        high_data = clean_block(
            high_data
        )

        low_data = df[
            [
                "condition",
                "key_resp_10.corr",
                "key_resp_10.rt"
            ]
        ].copy()

        low_data.columns = [
            "condition",
            "corr",
            "rt"
        ]

        low_data = clean_block(
            low_data
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

    return {

        "Participant":
            participant,

        "High_Neutral_Mean":
            high_scores["Neutral"],

        "High_Incongruent_Mean":
            high_scores["Incongruent"],

        "High_Congruent_Mean":
            high_scores["Congruent"],

        "High_Block_IF":
            high_scores["IF"],

        "High_Block_Facilitation":
            high_scores["Facilitation"],

        "Low_Neutral_Mean":
            low_scores["Neutral"],

        "Low_Incongruent_Mean":
            low_scores["Incongruent"],

        "Low_Congruent_Mean":
            low_scores["Congruent"],

        "Low_Block_IF":
            low_scores["IF"],

        "Low_Block_Facilitation":
            low_scores["Facilitation"]
    }


# PROCESS MULTIPLE FILES

def process_multiple_files(files):

    results = []

    for file in files:

        try:

            result = process_single_file(
                file
            )

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
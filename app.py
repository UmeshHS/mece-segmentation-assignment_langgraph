# Install dependencies (uncomment if running locally or in Colab)
# !pip install langgraph langchain-core pandas

from langgraph.graph import StateGraph, END
from typing import TypedDict
import pandas as pd
from google.colab import files

# Prompt user to upload CSV containing cart abandonment data
print("📂 Please upload your input CSV file...")
uploaded = files.upload()
input_file = list(uploaded.keys())[0]
df = pd.read_csv(input_file)


# Define state dictionary schema for the pipeline
class AudienceState(TypedDict):
    df: pd.DataFrame            # Original data
    segmented_df: pd.DataFrame  # Data with segment labels
    summary: pd.DataFrame       # Aggregated segment summary


# Load the uploaded data into the state
def initialize(state: AudienceState):
    state["df"] = df.copy()
    return state


# Segment users into 3 groups based on AOV and engagement score
def segment_users(state: AudienceState):
    data = state["df"].copy()

    def assign_segment(row):
        if row["avg_order_value"] > 3000:
            return "High AOV Abandoners"
        elif 1000 < row["avg_order_value"] <= 3000 and row["engagement_score"] > 0.5:
            return "Mid AOV Engaged"
        else:
            return "Other Bucket"

    data["segment"] = data.apply(assign_segment, axis=1)
    state["segmented_df"] = data
    return state


# Compute summary aggregations and score each segment
def compute_summary(state: AudienceState):
    seg = state["segmented_df"]

    summary = seg.groupby("segment").agg(
        Size=("user_id", "count"),
        avg_engagement=("engagement_score", "mean"),
        avg_profitability=("profitability_score", "mean"),
    ).reset_index()

    # Normalize engagement and profitability scores
    summary["Conv_Pot"] = summary["avg_engagement"] / summary["avg_engagement"].max()
    summary["Profitability"] = summary["avg_profitability"] / summary["avg_profitability"].max()

    # Weighted average for overall score
    summary["Overall Score"] = 0.5 * summary["Conv_Pot"] + 0.5 * summary["Profitability"]

    # Map rules applied to each segment for clarity
    rules_map = {
        "High AOV Abandoners": "AOV > 3000",
        "Mid AOV Engaged": "1000 < AOV <= 3000 & Engagement > 0.5",
        "Other Bucket": "ELSE",
    }
    summary["Rules Applied"] = summary["segment"].map(rules_map)

    # Mark segments with less than 10 users as invalid for demo purposes
    summary["Valid"] = summary["Size"].apply(lambda x: "No" if x < 10 else "Yes")

    # Select and rename columns for output
    columns = ["segment", "Rules Applied", "Size", "Conv_Pot", "Profitability", "Overall Score", "Valid"]
    summary = summary[columns].rename(columns={"segment": "Segment Name"})

    state["summary"] = summary
    return state


# Build the workflow graph and add nodes and edges
workflow = StateGraph(AudienceState)
workflow.add_node("initialize", initialize)
workflow.add_node("segment_users", segment_users)
workflow.add_node("compute_summary", compute_summary)

workflow.set_entry_point("initialize")
workflow.add_edge("initialize", "segment_users")
workflow.add_edge("segment_users", "compute_summary")
workflow.add_edge("compute_summary", END)

app = workflow.compile()

# Run the workflow and retrieve final summary
final_state = app.invoke({})
summary = final_state["summary"]

print("\n✅ Final Audience Strategy Table:")
print(summary)

# Save summary to CSV and prompt download in Colab
summary_file = "audience_strategy.csv"
summary.to_csv(summary_file, index=False)
files.download(summary_file)

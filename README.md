# mece-segmentation-assignment_langgraph

# MECE Audience Segmentation for Cart Abandoners

## Project Overview
This project implements a MECE (Mutually Exclusive, Collectively Exhaustive) audience segmentation solution targeting users who recently abandoned their shopping carts. The segmentation helps marketing teams tailor strategies for better customer retention through behavior and value-based classification.

---

## Features
- Filters users who abandoned carts within the last 7 days.
- Divides users into three clear segments:
  - **High AOV Abandoners:** Average order value greater than 3000.
  - **Mid AOV Engaged:** Average order value between 1000 and 3000 and high engagement.
  - **Other Bucket:** Remaining users.
- Computes conversion potential, profitability, and overall scores for each segment.
- Flags segments as valid or invalid based on minimum size constraints.
- Outputs a summarized CSV report for marketing use.

---

## Dataset
The input dataset should have the following columns:
- `user_id`: Unique user identifier
- `cart_abandoned_date`: Date of cart abandonment
- `last_order_date`: Date of last order placed
- `avg_order_value`: Average order value per user
- `sessions_last_30d`: Number of sessions in the last 30 days
- `num_cart_items`: Number of items in abandoned cart
- `engagement_score`: Engagement score (numeric)
- `profitability_score`: Profitability score (numeric)

---

## Getting Started

### Prerequisites
- Python 3.7 or above
- Install dependencies:
    pip install langgraph langchain-core pandas

### Running the Project
1. Upload your dataset CSV when prompted.
2. The segmentation pipeline will run automatically, segmenting users and computing scores.
3. Download the output CSV `audience_strategy.csv` containing segment summaries.

---

## Project Structure

- `app.py`: The main script that runs the LangGraph-based segmentation workflow.
- `cart_abandonment_demo.csv`: Sample/input dataset for cart abandoners.
- `README.md`: This file.

---

## How It Works
The core logic is encapsulated in a LangGraph workflow with the following nodes:
- **Initialize:** Loads and prepares input data.
- **Segment Users:** Applies MECE segmentation based on order value and engagement rules.
- **Compute Summary:** Aggregates segment size and scores, applies validity checks.

---

## Future Improvements
- Integrate machine learning-based segmentation.
- Connect the workflow with real-time marketing automation tools.
- Expand scoring with additional behavioral signals.

---

## Contact
For questions or contributions, open an issue or contact [Umesh h s & uhs260066@gmail.com].

---

## License
MIT License


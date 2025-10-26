# Metaculus Scripts

This folder contains utility scripts for working with Metaculus data.

## Metaculus Medaled User Predictions Aggregator

**File:** `metaculus_medaled_predictions.py`

This script fetches comments with predictions from a Metaculus question, filters for comments from users who have at least one medal, and provides aggregate prediction statistics from those users.

### Features

- Fetches all comments for a given Metaculus question
- Identifies users with medals (gold, silver, or bronze)
- Extracts predictions from comments made by medaled users
- Calculates aggregate statistics (mean, median, min, max, standard deviation)

### Usage

```bash
# Basic usage with question ID
python scripts/metaculus_medaled_predictions.py <question_id>

# Example with question ID
python scripts/metaculus_medaled_predictions.py 578

# Example with full question URL
python scripts/metaculus_medaled_predictions.py "https://www.metaculus.com/questions/578/"

# With API token for authenticated requests (optional)
python scripts/metaculus_medaled_predictions.py 578 YOUR_API_TOKEN
```

### Requirements

- Python 3.6+
- `requests` library

Install dependencies:
```bash
pip install -r requirements.txt
```

### API Endpoints Used

The script uses the following Metaculus API v2 endpoints:

- `GET /api2/questions/{id}/` - Fetch question details
- `GET /api2/comments/?question={id}` - Fetch comments for a question
- `GET /api2/users/{id}/` - Fetch user details and medal information

### Output

The script outputs:
1. Question details (title, type)
2. Total number of comments found
3. Number of unique medaled users
4. Number of predictions from medaled users
5. Aggregate statistics:
   - Count: Number of predictions
   - Mean: Average prediction
   - Median: Middle prediction value
   - Min/Max: Range of predictions
   - StdDev: Standard deviation

### Example Output

```
Processing question ID: 578

Fetching question details...
Question: Human extinction by 2100?
Type: binary

Fetching comments...
Found 145 total comments

Filtering comments by medaled users...
  - Found prediction 0.015 from user alice
  - Found prediction 0.022 from user bob
  - Found prediction 0.018 from user charlie

Found 3 unique users with medals
Found 3 predictions from medaled users

============================================================
AGGREGATE PREDICTIONS FROM MEDALED USERS
============================================================
Count:  3
Mean:   0.0183
Median: 0.0180
Min:    0.0150
Max:    0.0220
StdDev: 0.0036
============================================================
```

### Notes

- The Metaculus API documentation is still evolving, so some features may change
- Not all comments contain prediction snapshots; the script handles this gracefully
- User medal information is cached to avoid repeated API calls
- The script supports both public and authenticated API access
- For binary questions, predictions are typically in the range [0, 1]

### Troubleshooting

**No predictions found:**
- Some comments may not include prediction snapshots
- Predictions might be stored separately from comments in the API
- The question type might not support the expected prediction format

**API errors:**
- Rate limiting: Add delays between requests or use an API token
- 404 errors: The question or user might not exist or be private
- 403 errors: Some endpoints may require authentication

### Future Enhancements

Potential improvements:
- Support for different question types (multiple choice, numeric, date)
- Weighting predictions by user track record
- Export results to CSV/JSON
- Caching of API responses
- Support for prediction history over time

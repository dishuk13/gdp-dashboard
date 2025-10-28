#!/usr/bin/env python3
"""
Metaculus Medaled User Predictions Aggregator

This script fetches comments with predictions from a Metaculus question,
filters for comments from users who have at least one medal, and provides
an aggregate prediction from those users.

Usage:
    python metaculus_medaled_predictions.py <question_id_or_url>

Example:
    python metaculus_medaled_predictions.py 578
    python metaculus_medaled_predictions.py https://www.metaculus.com/questions/578/
"""

import sys
import re
import requests
import statistics
from typing import List, Dict, Any, Optional
from datetime import datetime


class MetaculusAPI:
    """Wrapper for Metaculus API interactions."""

    BASE_URL = "https://www.metaculus.com/api2"

    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the API client.

        Args:
            api_token: Optional API token for authenticated requests
        """
        self.session = requests.Session()
        if api_token:
            self.session.headers.update({
                'Authorization': f'Token {api_token}'
            })

    def get_question(self, question_id: int) -> Dict[str, Any]:
        """
        Fetch question details from Metaculus API.

        Args:
            question_id: The question ID

        Returns:
            Question data dictionary
        """
        url = f"{self.BASE_URL}/questions/{question_id}/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_comments(self, question_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch all comments for a question.
        Tries multiple endpoint approaches to handle API variations.

        Args:
            question_id: The question ID
            limit: Number of comments per request

        Returns:
            List of comment dictionaries
        """
        # Try multiple approaches to fetch comments
        approaches = [
            # Approach 1: on_post parameter (most likely to work)
            ('on_post', f"{self.BASE_URL}/comments/", {'on_post': question_id, 'limit': limit}),
            # Approach 2: question parameter
            ('question', f"{self.BASE_URL}/comments/", {'question': question_id, 'limit': limit}),
            # Approach 3: nested endpoint under posts
            ('nested_posts', f"{self.BASE_URL}/posts/{question_id}/comments/", {'limit': limit}),
        ]

        last_error = None

        for approach_name, url, params in approaches:
            try:
                all_comments = []
                current_params = params.copy()

                while True:
                    response = self.session.get(url, params=current_params)
                    response.raise_for_status()
                    data = response.json()

                    # Handle both list and dict responses
                    if isinstance(data, list):
                        all_comments.extend(data)
                        break  # Lists don't have pagination
                    elif isinstance(data, dict):
                        results = data.get('results', [])
                        all_comments.extend(results)

                        # Check if there's a next page
                        next_url = data.get('next')
                        if not next_url:
                            break

                        # Extract cursor from next URL
                        if 'cursor=' in next_url:
                            cursor = next_url.split('cursor=')[1].split('&')[0]
                            current_params['cursor'] = cursor
                            # Remove original filter param after first request
                            current_params.pop('question', None)
                            current_params.pop('on_post', None)
                        else:
                            break
                    else:
                        break

                # If we got here without an exception, it worked!
                if all_comments or approach_name == approaches[-1][0]:
                    # Success! or last attempt
                    return all_comments

            except requests.exceptions.HTTPError as e:
                last_error = e
                if e.response.status_code == 405:
                    # Method not allowed, try next approach
                    continue
                elif e.response.status_code == 404:
                    # Not found, try next approach
                    continue
                else:
                    # Other HTTP error, might be more serious
                    raise
            except Exception as e:
                last_error = e
                continue

        # If all approaches failed, raise the last error
        if last_error:
            print(f"\n⚠️  Warning: Could not fetch comments using standard approaches.")
            print(f"   Last error: {last_error}")
            print(f"   This may mean comments are not accessible via the API,")
            print(f"   or the API structure has changed.")
            print(f"   Run 'python scripts/test_metaculus_api.py {question_id}' for diagnostics.")

        return []

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Fetch user details from Metaculus API.

        Args:
            user_id: The user ID

        Returns:
            User data dictionary
        """
        url = f"{self.BASE_URL}/users/{user_id}/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()


def extract_question_id(input_str: str) -> int:
    """
    Extract question ID from URL or ID string.

    Args:
        input_str: Question ID or Metaculus question URL

    Returns:
        Question ID as integer

    Raises:
        ValueError: If question ID cannot be extracted
    """
    # If it's already a number
    if input_str.isdigit():
        return int(input_str)

    # Try to extract from URL
    match = re.search(r'/questions/(\d+)/', input_str)
    if match:
        return int(match.group(1))

    raise ValueError(f"Could not extract question ID from: {input_str}")


def has_medals(user_data: Dict[str, Any]) -> bool:
    """
    Check if a user has at least one medal.

    Args:
        user_data: User data dictionary from API

    Returns:
        True if user has at least one medal, False otherwise
    """
    # Check for medals in various possible locations in the API response
    # The exact structure may vary, so we check multiple places

    # Check if there's a medals field
    if 'medals' in user_data:
        medals = user_data['medals']
        if isinstance(medals, list) and len(medals) > 0:
            return True
        if isinstance(medals, dict) and any(medals.values()):
            return True

    # Check medal counts (gold_medals, silver_medals, bronze_medals, etc.)
    medal_fields = ['gold_medals', 'silver_medals', 'bronze_medals', 'total_medals']
    for field in medal_fields:
        if field in user_data and user_data[field] and user_data[field] > 0:
            return True

    # Check if there's a medal_count field
    if 'medal_count' in user_data and user_data['medal_count'] > 0:
        return True

    return False


def extract_prediction_from_comment(comment: Dict[str, Any]) -> Optional[float]:
    """
    Extract prediction value from a comment if it contains one.

    Args:
        comment: Comment data dictionary

    Returns:
        Prediction value (0-1 for binary questions) or None if no prediction found
    """
    # Check if comment has a prediction_snapshot field
    if 'prediction_snapshot' in comment and comment['prediction_snapshot']:
        snapshot = comment['prediction_snapshot']

        # For binary questions, look for probability
        if isinstance(snapshot, dict):
            if 'probability' in snapshot:
                return snapshot['probability']
            elif 'prediction' in snapshot:
                return snapshot['prediction']
            elif 'q2' in snapshot:  # q2 is median
                return snapshot['q2']
        elif isinstance(snapshot, (int, float)):
            return float(snapshot)

    # Check for prediction in comment metadata
    if 'prediction' in comment and comment['prediction'] is not None:
        pred = comment['prediction']
        if isinstance(pred, dict) and 'probability' in pred:
            return pred['probability']
        elif isinstance(pred, (int, float)):
            return float(pred)

    return None


def aggregate_predictions(predictions: List[float]) -> Dict[str, float]:
    """
    Calculate aggregate statistics from predictions.

    Args:
        predictions: List of prediction values

    Returns:
        Dictionary with aggregate statistics
    """
    if not predictions:
        return {}

    return {
        'mean': statistics.mean(predictions),
        'median': statistics.median(predictions),
        'min': min(predictions),
        'max': max(predictions),
        'count': len(predictions),
        'stdev': statistics.stdev(predictions) if len(predictions) > 1 else 0.0
    }


def main(question_input: str, api_token: Optional[str] = None):
    """
    Main function to process Metaculus question and aggregate medaled user predictions.

    Args:
        question_input: Question ID or URL
        api_token: Optional API token for authenticated requests
    """
    try:
        question_id = extract_question_id(question_input)
        print(f"Processing question ID: {question_id}")

        # Initialize API client
        api = MetaculusAPI(api_token)

        # Fetch question details
        print("\nFetching question details...")
        question = api.get_question(question_id)
        print(f"Question: {question.get('title', 'Unknown')}")
        print(f"Type: {question.get('type', 'Unknown')}")

        # Fetch comments
        print("\nFetching comments...")
        comments = api.get_comments(question_id)
        print(f"Found {len(comments)} total comments")

        # Filter comments by medaled users and extract predictions
        print("\nFiltering comments by medaled users...")
        medaled_user_predictions = []
        medaled_users = set()
        user_cache = {}  # Cache user data to avoid repeated API calls

        for comment in comments:
            author_id = comment.get('author')
            if not author_id:
                continue

            # Check cache first
            if author_id not in user_cache:
                try:
                    user_data = api.get_user(author_id)
                    user_cache[author_id] = user_data
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 404:
                        # User not found, skip
                        user_cache[author_id] = None
                        continue
                    raise

            user_data = user_cache[author_id]
            if user_data is None:
                continue

            # Check if user has medals
            if has_medals(user_data):
                medaled_users.add(author_id)

                # Try to extract prediction from comment
                prediction = extract_prediction_from_comment(comment)
                if prediction is not None:
                    medaled_user_predictions.append(prediction)
                    print(f"  - Found prediction {prediction:.3f} from user {user_data.get('username', author_id)}")

        print(f"\nFound {len(medaled_users)} unique users with medals")
        print(f"Found {len(medaled_user_predictions)} predictions from medaled users")

        # Calculate aggregates
        if medaled_user_predictions:
            print("\n" + "="*60)
            print("AGGREGATE PREDICTIONS FROM MEDALED USERS")
            print("="*60)

            aggregates = aggregate_predictions(medaled_user_predictions)
            print(f"Count:  {aggregates['count']}")
            print(f"Mean:   {aggregates['mean']:.4f}")
            print(f"Median: {aggregates['median']:.4f}")
            print(f"Min:    {aggregates['min']:.4f}")
            print(f"Max:    {aggregates['max']:.4f}")
            print(f"StdDev: {aggregates['stdev']:.4f}")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("No predictions found from medaled users in comments")
            print("="*60)
            print("\nNote: This may be because:")
            print("  1. Comments don't contain prediction snapshots")
            print("  2. Predictions are stored separately from comments")
            print("  3. The API structure differs from expected format")
            print("\nConsider checking the question directly on Metaculus.com")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"API Error: {e}", file=sys.stderr)
        print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    question_input = sys.argv[1]
    api_token = sys.argv[2] if len(sys.argv) > 2 else None

    main(question_input, api_token)

# Troubleshooting Metaculus API Issues

## 405 Method Not Allowed Error

If you're getting a **405 error** when trying to fetch comments, this means the HTTP method (GET) is not allowed for the endpoint you're trying to access, or the endpoint structure is different than expected.

### Diagnostic Steps

Run the test script to identify which endpoint structure works:

```bash
# Test without API token
python scripts/test_metaculus_api.py 578

# Test with API token (recommended)
python scripts/test_metaculus_api.py 578 YOUR_API_TOKEN
```

The script will test 5 different approaches:
1. `/api2/comments/?question={id}` - Standard query parameter
2. `/api2/posts/{id}/comments/` - Nested endpoint structure
3. `/api2/questions/{id}/` - Check if comments are nested in question
4. `/api2/posts/{id}/` - Alternative post endpoint
5. `/api2/comments/?on_post={id}` - Alternative parameter name

### Common Issues and Solutions

#### Issue 1: Wrong Parameter Name

The API might use `on_post` instead of `question` as the query parameter.

**Solution:**
```python
# Instead of:
params = {'question': question_id}

# Try:
params = {'on_post': question_id}
```

#### Issue 2: Different Endpoint Structure

The comments might be at a different path, such as nested under posts.

**Solution:**
```python
# Instead of:
url = f"{BASE_URL}/comments/?question={id}"

# Try:
url = f"{BASE_URL}/posts/{id}/comments/"
```

#### Issue 3: Authentication Required

Some endpoints require authentication even for read operations.

**Solution:**
Always include your API token:
```python
headers = {'Authorization': f'Token {YOUR_API_TOKEN}'}
```

#### Issue 4: Comments Not Separate Endpoint

Comments might be embedded in the question/post response itself.

**Solution:**
Check the question response for comment-related fields:
```python
question = api.get_question(question_id)
# Check for: comment_count, comments, top_comments, etc.
```

### Alternative Approach: Use Question Data

If the comments endpoint continues to fail, you can still aggregate predictions by:

1. **Using the community prediction** from the question data itself:
```python
question = api.get_question(question_id)
community_pred = question.get('community_prediction')
```

2. **Fetching individual user predictions** (if available through a different endpoint)

3. **Using prediction history** from the question response:
```python
pred_history = question.get('prediction_timeseries', [])
```

### Getting Help

1. **Check the official API docs**: https://www.metaculus.com/api2/schema/redoc/
2. **Try the endpoint in a browser**: Visit the URL directly to see if it works
3. **Check API status**: Make sure Metaculus API is operational
4. **Rate limiting**: If you made many requests, you might be rate-limited

### API Token

To get an API token:
1. Log in to Metaculus.com
2. Go to your account settings
3. Find the API section (or developer section)
4. Generate or copy your API token

### Example Working Request

Based on search results, this format has been seen working:

```python
import requests

url = "https://www.metaculus.com/api2/comments/"
params = {
    'on_post': 956,  # or 'question': 956
    'limit': 100
}
headers = {
    'Authorization': 'Token YOUR_TOKEN_HERE'
}

response = requests.get(url, params=params, headers=headers)
print(response.status_code, response.json())
```

### Contact

If none of these solutions work:
- Open an issue on the Metaculus GitHub: https://github.com/Metaculus/metaculus
- Check the Metaculus Discord or community forums
- Verify with other Metaculus API users

## Known Limitations

1. **API Evolution**: The Metaculus API is still being actively developed
2. **Documentation**: Not all endpoints are fully documented
3. **Prediction Snapshots**: Not all comments contain prediction data
4. **Medal Information**: Medal data structure may vary by user
5. **Rate Limits**: Excessive requests may be throttled

#!/usr/bin/env python3
"""
Diagnostic script to test Metaculus API endpoints for fetching comments.

This script tests various approaches to fetching comments from the Metaculus API
to determine which method works correctly.

Usage:
    python test_metaculus_api.py <question_id> [api_token]
"""

import sys
import requests
import json


def test_comments_endpoint_1(question_id, api_token=None):
    """Test /api2/comments/ with question parameter"""
    print("\n" + "="*60)
    print("TEST 1: /api2/comments/ with question parameter")
    print("="*60)

    url = "https://www.metaculus.com/api2/comments/"
    params = {'question': question_id, 'limit': 10}

    headers = {}
    if api_token:
        headers['Authorization'] = f'Token {api_token}'

    try:
        print(f"URL: {url}")
        print(f"Params: {params}")
        print(f"Headers: {headers}")

        response = requests.get(url, params=params, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.ok:
            data = response.json()
            print(f"✅ SUCCESS!")
            print(f"Number of results: {len(data.get('results', []))}")
            print(f"Total count: {data.get('count', 'N/A')}")
            if data.get('results'):
                print(f"First comment ID: {data['results'][0].get('id')}")
            return True, data
        else:
            print(f"❌ FAILED: {response.status_code} {response.reason}")
            print(f"Response: {response.text[:500]}")
            return False, None

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, None


def test_comments_endpoint_2(question_id, api_token=None):
    """Test /api2/posts/{id}/comments/"""
    print("\n" + "="*60)
    print("TEST 2: /api2/posts/{id}/comments/")
    print("="*60)

    url = f"https://www.metaculus.com/api2/posts/{question_id}/comments/"

    headers = {}
    if api_token:
        headers['Authorization'] = f'Token {api_token}'

    try:
        print(f"URL: {url}")
        print(f"Headers: {headers}")

        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")

        if response.ok:
            data = response.json()
            print(f"✅ SUCCESS!")
            print(f"Data type: {type(data)}")
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
            return True, data
        else:
            print(f"❌ FAILED: {response.status_code} {response.reason}")
            print(f"Response: {response.text[:500]}")
            return False, None

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, None


def test_question_response(question_id, api_token=None):
    """Test if comments are nested in question response"""
    print("\n" + "="*60)
    print("TEST 3: Check if comments in /api2/questions/{id}/")
    print("="*60)

    url = f"https://www.metaculus.com/api2/questions/{question_id}/"

    headers = {}
    if api_token:
        headers['Authorization'] = f'Token {api_token}'

    try:
        print(f"URL: {url}")
        print(f"Headers: {headers}")

        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")

        if response.ok:
            data = response.json()
            print(f"✅ Question fetched successfully!")
            print(f"Question title: {data.get('title', 'N/A')}")

            # Check for comment-related fields
            print("\nSearching for comment-related fields...")
            comment_fields = [k for k in data.keys() if 'comment' in k.lower()]
            if comment_fields:
                print(f"Found comment fields: {comment_fields}")
                for field in comment_fields:
                    print(f"  {field}: {type(data[field])} = {str(data[field])[:100]}")
            else:
                print("No comment fields found in response")

            # Print all top-level keys
            print(f"\nAll keys in response: {list(data.keys())[:20]}")

            return True, data
        else:
            print(f"❌ FAILED: {response.status_code} {response.reason}")
            return False, None

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, None


def test_api2_posts(question_id, api_token=None):
    """Test /api2/posts/{id}/ endpoint"""
    print("\n" + "="*60)
    print("TEST 4: /api2/posts/{id}/")
    print("="*60)

    url = f"https://www.metaculus.com/api2/posts/{question_id}/"

    headers = {}
    if api_token:
        headers['Authorization'] = f'Token {api_token}'

    try:
        print(f"URL: {url}")
        print(f"Headers: {headers}")

        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")

        if response.ok:
            data = response.json()
            print(f"✅ SUCCESS!")

            # Check for comment-related fields
            comment_fields = [k for k in data.keys() if 'comment' in k.lower()]
            if comment_fields:
                print(f"Found comment fields: {comment_fields}")

            print(f"All keys: {list(data.keys())[:20]}")
            return True, data
        else:
            print(f"❌ FAILED: {response.status_code} {response.reason}")
            return False, None

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, None


def test_comments_with_on_post(question_id, api_token=None):
    """Test /api2/comments/ with on_post parameter"""
    print("\n" + "="*60)
    print("TEST 5: /api2/comments/ with on_post parameter")
    print("="*60)

    url = "https://www.metaculus.com/api2/comments/"
    params = {'on_post': question_id, 'limit': 10}

    headers = {}
    if api_token:
        headers['Authorization'] = f'Token {api_token}'

    try:
        print(f"URL: {url}")
        print(f"Params: {params}")

        response = requests.get(url, params=params, headers=headers)
        print(f"Status Code: {response.status_code}")

        if response.ok:
            data = response.json()
            print(f"✅ SUCCESS!")
            print(f"Number of results: {len(data.get('results', []))}")
            return True, data
        else:
            print(f"❌ FAILED: {response.status_code} {response.reason}")
            print(f"Response: {response.text[:500]}")
            return False, None

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, None


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_metaculus_api.py <question_id> [api_token]")
        sys.exit(1)

    question_id = sys.argv[1]
    api_token = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"\n🔍 Testing Metaculus API for question ID: {question_id}")
    if api_token:
        print(f"   Using API token: {api_token[:10]}...")
    else:
        print("   No API token provided (using unauthenticated requests)")

    # Run all tests
    tests = [
        test_comments_endpoint_1,
        test_comments_endpoint_2,
        test_question_response,
        test_api2_posts,
        test_comments_with_on_post
    ]

    results = {}
    for test in tests:
        success, data = test(question_id, api_token)
        results[test.__name__] = (success, data)

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    successful_tests = [name for name, (success, _) in results.items() if success]

    if successful_tests:
        print(f"\n✅ {len(successful_tests)} test(s) succeeded:")
        for name in successful_tests:
            print(f"   - {name}")

        print("\n💡 Recommended approach:")
        print(f"   Use: {successful_tests[0]}")
    else:
        print("\n❌ All tests failed!")
        print("\nPossible reasons:")
        print("   1. The question ID might be invalid")
        print("   2. The API might require authentication for all comment requests")
        print("   3. Comments endpoint might have changed")
        print("   4. Rate limiting might be in effect")
        print("\nTry:")
        print("   - Using a valid API token")
        print("   - Checking https://www.metaculus.com/api2/schema/redoc/")
        print("   - Testing with a different question ID")


if __name__ == "__main__":
    main()

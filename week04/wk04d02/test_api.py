"""
Test Script for W4D2 Breakout Activity 1
========================================

This script demonstrates and tests all API endpoints.
Run this after starting the API server (python breakout03.py).

Usage:
    python test_api.py
"""

import requests
import json
from typing import Dict, Any

# Base URL for the API
BASE_URL = "http://localhost:8000"


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_response(response: requests.Response, show_body: bool = True):
    """Print formatted response information."""
    print(f"\nStatus Code: {response.status_code}")
    if show_body and response.text:
        try:
            data = response.json()
            print(f"Response Body:\n{json.dumps(data, indent=2)}")
        except:
            print(f"Response Body: {response.text}")


def test_root_endpoint():
    """Test the root endpoint."""
    print_section("TEST 1: Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    assert response.status_code == 200, "Root endpoint should return 200"
    print("✅ PASSED")


def test_health_check():
    """Test the health check endpoint."""
    print_section("TEST 2: Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    assert response.status_code == 200, "Health check should return 200"
    data = response.json()
    assert data["status"] == "healthy", "Status should be healthy"
    print("✅ PASSED")


def test_get_personal_info():
    """Test getting personal information."""
    print_section("TEST 3: GET Personal Information")
    response = requests.get(f"{BASE_URL}/me")
    print_response(response)
    assert response.status_code == 200, "GET /me should return 200"
    data = response.json()
    assert "name" in data, "Response should contain 'name'"
    assert "age" in data, "Response should contain 'age'"
    print("✅ PASSED")


def test_update_personal_info():
    """Test updating personal information."""
    print_section("TEST 4: PUT Personal Information")
    
    updated_info = {
        "name": "Test User",
        "age": 30,
        "location": "Test City",
        "occupation": "Test Engineer",
        "bio": "Testing the API"
    }
    
    response = requests.put(
        f"{BASE_URL}/me",
        json=updated_info
    )
    print_response(response)
    assert response.status_code == 200, "PUT /me should return 200"
    data = response.json()
    assert data["name"] == "Test User", "Name should be updated"
    print("✅ PASSED")


def test_get_all_hobbies():
    """Test getting all hobbies."""
    print_section("TEST 5: GET All Hobbies")
    response = requests.get(f"{BASE_URL}/hobbies")
    print_response(response)
    assert response.status_code == 200, "GET /hobbies should return 200"
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    print(f"Found {len(data)} hobbies")
    print("✅ PASSED")


def test_filter_hobbies_by_skill():
    """Test filtering hobbies by skill level."""
    print_section("TEST 6: Filter Hobbies by Skill Level")
    response = requests.get(
        f"{BASE_URL}/hobbies",
        params={"skill_level": "intermediate"}
    )
    print_response(response)
    assert response.status_code == 200, "Filtering should return 200"
    data = response.json()
    for hobby in data:
        assert hobby["skill_level"] == "intermediate", "All hobbies should be intermediate"
    print(f"Found {len(data)} intermediate hobbies")
    print("✅ PASSED")


def test_filter_hobbies_by_experience():
    """Test filtering hobbies by minimum experience."""
    print_section("TEST 7: Filter Hobbies by Experience")
    min_exp = 2
    response = requests.get(
        f"{BASE_URL}/hobbies",
        params={"min_experience": min_exp}
    )
    print_response(response)
    assert response.status_code == 200, "Filtering should return 200"
    data = response.json()
    for hobby in data:
        assert hobby["years_experience"] >= min_exp, f"Experience should be >= {min_exp}"
    print(f"Found {len(data)} hobbies with {min_exp}+ years experience")
    print("✅ PASSED")


def test_get_specific_hobby():
    """Test getting a specific hobby by ID."""
    print_section("TEST 8: GET Specific Hobby")
    response = requests.get(f"{BASE_URL}/hobbies/1")
    print_response(response)
    assert response.status_code == 200, "GET /hobbies/1 should return 200"
    data = response.json()
    assert data["id"] == 1, "Hobby ID should be 1"
    print("✅ PASSED")


def test_get_nonexistent_hobby():
    """Test getting a hobby that doesn't exist."""
    print_section("TEST 9: GET Nonexistent Hobby (404)")
    response = requests.get(f"{BASE_URL}/hobbies/9999")
    print_response(response)
    assert response.status_code == 404, "Should return 404 for nonexistent hobby"
    print("✅ PASSED")


def test_create_hobby():
    """Test creating a new hobby."""
    print_section("TEST 10: POST Create New Hobby")
    
    new_hobby = {
        "name": "Guitar",
        "skill_level": "beginner",
        "years_experience": 1,
        "description": "Learning acoustic guitar"
    }
    
    response = requests.post(
        f"{BASE_URL}/hobbies",
        json=new_hobby
    )
    print_response(response)
    assert response.status_code == 201, "POST should return 201 Created"
    data = response.json()
    assert "id" in data, "Response should contain assigned ID"
    assert data["name"] == "Guitar", "Name should match"
    print(f"Created hobby with ID: {data['id']}")
    print("✅ PASSED")
    
    return data["id"]  # Return ID for later tests


def test_update_hobby(hobby_id: int):
    """Test updating a hobby."""
    print_section("TEST 11: PUT Update Hobby")
    
    update_data = {
        "skill_level": "intermediate",
        "years_experience": 2
    }
    
    response = requests.put(
        f"{BASE_URL}/hobbies/{hobby_id}",
        json=update_data
    )
    print_response(response)
    assert response.status_code == 200, "PUT should return 200"
    data = response.json()
    assert data["skill_level"] == "intermediate", "Skill level should be updated"
    assert data["years_experience"] == 2, "Experience should be updated"
    print("✅ PASSED")


def test_delete_hobby(hobby_id: int):
    """Test deleting a hobby."""
    print_section("TEST 12: DELETE Hobby")
    
    response = requests.delete(f"{BASE_URL}/hobbies/{hobby_id}")
    print_response(response, show_body=False)
    assert response.status_code == 204, "DELETE should return 204 No Content"
    
    # Verify it's deleted
    verify_response = requests.get(f"{BASE_URL}/hobbies/{hobby_id}")
    assert verify_response.status_code == 404, "Deleted hobby should return 404"
    print("✅ PASSED")


def test_delete_nonexistent_hobby():
    """Test deleting a hobby that doesn't exist."""
    print_section("TEST 13: DELETE Nonexistent Hobby (404)")
    
    response = requests.delete(f"{BASE_URL}/hobbies/9999")
    print_response(response)
    assert response.status_code == 404, "Should return 404 for nonexistent hobby"
    print("✅ PASSED")


def test_statistics():
    """Test the statistics endpoint."""
    print_section("TEST 14: GET Statistics")
    
    response = requests.get(f"{BASE_URL}/stats")
    print_response(response)
    assert response.status_code == 200, "Stats endpoint should return 200"
    data = response.json()
    assert "total_hobbies" in data, "Should include total hobbies"
    assert "average_experience" in data, "Should include average experience"
    assert "skill_level_distribution" in data, "Should include skill distribution"
    print("✅ PASSED")


def test_invalid_skill_level():
    """Test filtering with invalid skill level."""
    print_section("TEST 15: Invalid Skill Level Filter (400)")
    
    response = requests.get(
        f"{BASE_URL}/hobbies",
        params={"skill_level": "invalid"}
    )
    print_response(response)
    assert response.status_code == 400, "Should return 400 for invalid skill level"
    print("✅ PASSED")


def test_invalid_hobby_creation():
    """Test creating a hobby with invalid data."""
    print_section("TEST 16: Invalid Hobby Creation (422)")
    
    invalid_hobby = {
        "name": "Test",
        "skill_level": "invalid_level",  # Invalid
        "years_experience": -5  # Invalid
    }
    
    response = requests.post(
        f"{BASE_URL}/hobbies",
        json=invalid_hobby
    )
    print_response(response)
    assert response.status_code == 422, "Should return 422 for validation error"
    print("✅ PASSED")


def run_all_tests():
    """Run all tests in sequence."""
    print("\n" + "🎯"*30)
    print("  W4D2 BREAKOUT ACTIVITY 1 - API TEST SUITE")
    print("🎯"*30)
    
    try:
        # Check if server is running
        try:
            requests.get(f"{BASE_URL}/health", timeout=2)
        except requests.exceptions.ConnectionError:
            print("\n❌ ERROR: API server is not running!")
            print("Please start the server with: python breakout03.py")
            return
        
        # Run all tests
        test_root_endpoint()
        test_health_check()
        test_get_personal_info()
        test_update_personal_info()
        test_get_all_hobbies()
        test_filter_hobbies_by_skill()
        test_filter_hobbies_by_experience()
        test_get_specific_hobby()
        test_get_nonexistent_hobby()
        
        # Create, update, and delete a hobby
        hobby_id = test_create_hobby()
        test_update_hobby(hobby_id)
        test_delete_hobby(hobby_id)
        
        test_delete_nonexistent_hobby()
        test_statistics()
        test_invalid_skill_level()
        test_invalid_hobby_creation()
        
        # Summary
        print("\n" + "="*60)
        print("  ✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n🎉 Congratulations! Your API implementation is working correctly!")
        print("\n📚 Next Steps:")
        print("   1. Explore the API documentation at http://localhost:8000/docs")
        print("   2. Try the challenge extensions from the assignment")
        print("   3. Consider adding authentication and database persistence")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    run_all_tests()

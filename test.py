import requests

# Sample test
test_response = """{
  "response": "{\\"name\\": \\"John Doe\\", \\"education\\": {...}}"
}"""

data = json.loads(test_response)
json_str = data["response"]  # Get the inner JSON string
result = json.loads(json_str)  # Parse actual content
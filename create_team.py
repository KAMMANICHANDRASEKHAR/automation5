import os
import sys
import requests
from requests.auth import HTTPBasicAuth

# Fetch sensitive data from environment variables
sitename = os.getenv('SITENAME')
org_id = os.getenv('ORG_ID')
email = os.getenv('EMAIL')
api_token = os.getenv('API_TOKEN')
site_id = os.getenv('SITE_ID')

# Get the display_name from command-line arguments
if len(sys.argv) != 2:
    print("Usage: python create_team.py <display_name>")
    sys.exit(1)

display_name = sys.argv[1]

# Other details
description = 'This is an example team description.'
team_type = 'OPEN'

# Construct the URL for checking if the team exists
check_url = f'https://{sitename}.atlassian.net/gateway/api/public/teams/v1/org/{org_id}/teams/search'

# Headers for the request
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Data payload for searching the team
search_params = {
    'query': display_name
}

# Make the GET request to check if the team already exists
response = requests.get(
    check_url,
    headers=headers,
    auth=HTTPBasicAuth(email, api_token),
    params=search_params
)

# Check if the team exists
if response.status_code == 200:
    teams = response.json().get('teams', [])
    for team in teams:
        if team.get('displayName') == display_name:
            print(f"Team '{display_name}' already exists.")
            sys.exit(1)
else:
    print("Failed to check for existing team.")
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    sys.exit(1)

# If the team does not exist, proceed to create it
create_url = f'https://{sitename}.atlassian.net/gateway/api/public/teams/v1/org/{org_id}/teams/'

# Data payload for creating the team
data = {
    "description": description,
    "displayName": display_name,
    "siteId": site_id,
    "teamType": team_type
}

# Make the POST request to create the team
response = requests.post(
    create_url,
    headers=headers,
    auth=HTTPBasicAuth(email, api_token),
    json=data
)

# Print the response
if response.status_code == 201:
    print("Team created successfully!")
    print("Response:", response.json())
else:
    print("Failed to create team.")
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    sys.exit(1)

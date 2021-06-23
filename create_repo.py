import os
import sys
import json
import requests


# Read a local file containing user authentication token
def GetToken():
    # Equivilant of stepping out 2 directories ("../../")
    token_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    # Name of text file storing GitHub API key
    token_file = os.path.join(token_dir, 'github.txt')
    try:
        with open(token_file, 'r') as f:
            token = f.readlines()[0]
    except:
        print('No file found: {}'.format(token_dir))
        sys.exit()
    return token

# --------------------------------------------------------------

# Check the status of a response for any errors and
#   print them to the console if any occur.
def ResponseStatus(response):
    if 'errors' in json.loads(response.text):
        errors = ''
        for e in json.loads(response.text)['errors']:
            if errors == '':
                errors = "{}".format(e['message'])
            else:
                errors = errors + ". {}".format(e['message'])
        print("[{}] {}\nError(s): {}".format(response.status_code, json.loads(response.text)['message'], errors))
        sys.exit()

# --------------------------------------------------------------

# Send a POST request and check the response for errors
def CreateRepo(url, data, headers):
    response = requests.post(url, data = json.dumps(data), headers = headers)
    ResponseStatus(response)
    print('Successfully created!')
    response_json = json.loads(response.text)
    print('  > {}'.format(response_json['clone_url']))

# --------------------------------------------------------------

# Send a DELETE request
def DelRepo(url, headers):
    try:
        requests.delete(url, headers = headers)
    except requests.exceptions.RequestException as e:
        print('Failed to delete <{}>'.format(url))
        print(e)

# --------------------------------------------------------------

# Ask the user if they want to delete the repository 
#   that was just created
def RevertChanges():
    while True:
        revert = input("Do you want to keep these changes [Y/n]: ").lstrip().rstrip()
        if not (revert.upper() == 'Y' or revert.upper() == 'N'):
            print('Error: please enter [Y] or [n]')
        else:
            if revert.upper() == 'N':
                DelRepo(
                    base_url + "/repos/{}/{}".format(username, repo_name), 
                    {'Authorization': "token {}".format(token)}
                )
                print('Repository deleted.')
            break

# --------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 48)
    print('Create or delete a GitHub repository from the command line')
    print('-' * 48)

    username = 'geocoug'
    token = GetToken()
    base_url = 'https://api.github.com'
    
    repo_name = input('Enter a repository name: ').lstrip().rstrip()
    while True:
        private = input('Private repository [Y/n]: ').lstrip().rstrip()
        if not (private.upper() == 'Y' or private.upper() == 'N'):
            print('Error: please enter [Y] or [n]')
        else:
            break
    if private.upper() == 'Y':
        private = True
    else:
        private = False
    # Create a repo
    CreateRepo(
        base_url + '/user/repos', 
        {"name": repo_name, "private": private}, 
        {'Authorization': "token {}".format(token)}
    )
    # Ask user if they want to keep these changes
    RevertChanges()

    print('Done.')
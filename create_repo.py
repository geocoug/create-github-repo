#!/usr/bin/env python3

import json
import logging
import os

import requests

logging.basicConfig(level=logging.INFO, format="%(message)s")

base_url = "https://api.github.com"


def GetAuth() -> tuple:
    """Read a local file containing username and authentication token"""
    # Name of file storing GitHub token
    auth_file = os.path.join(
        os.path.dirname(os.path.dirname(os.getcwd())), "github.txt"
    )
    try:
        with open(auth_file, "r") as f:
            auth = f.readlines()
    except FileExistsError as e:
        raise e
    try:
        token = auth[0].strip()
        username = auth[1].strip()
    except Exception as e:
        raise e
    return username, token


def ResponseStatus(response: requests.models.Response) -> None:
    """Check the status of a response for any errors and
    print them to the console if any occur."""
    if "errors" in json.loads(response.text):
        errors = ""
        for e in json.loads(response.text)["errors"]:
            if errors == "":
                errors = f"{e['message']}"
            else:
                errors = errors + f". {e['message']}"
        raise Exception(
            f"""[{response.status_code}] {json.loads(response.text)['message']}\n
            Error(s): {errors}"""
        )


def CreateRepo(url: str, data: dict, headers: dict) -> None:
    """Send a POST request and check the response for errors"""
    response = requests.post(url, data=json.dumps(data), headers=headers)
    ResponseStatus(response)
    logging.info("Successfully created!")
    response_json = json.loads(response.text)
    logging.info(f"  > {response_json['clone_url']}")


def DeleteRepo(url: str, headers: dict) -> None:
    """Send a DELETE request"""
    try:
        requests.delete(url, headers=headers)
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException(f"Failed to delete <{url}>")


def RevertChanges(username: str, token: str, repo_name: str) -> None:
    """Ask the user if they want to delete the repository
    that was created."""
    while True:
        revert = input("Do you want to keep these changes [Y/n]: ").strip()
        if not (revert.upper() == "Y" or revert.upper() == "N"):
            logging.warning("Error: please enter [Y] or [n]")
        else:
            if revert.upper() == "N":
                DeleteRepo(
                    f"{base_url}/repos/{username}/{repo_name}",
                    {"Authorization": f"token {token}"},
                )
                logging.info("Repository deleted.")
            break


def main() -> None:
    """Main function"""
    username, token = GetAuth()

    repo_name = input("Enter a repository name: ").strip()
    while True:
        private = input("Private repository [Y/n]: ").strip()
        if not (private.upper() == "Y" or private.upper() == "N"):
            print("Error: please enter [Y] or [n]")
        else:
            break
    if private.upper() == "Y":
        private = True
    else:
        private = False
    repo_desc = input("Description (optional): ").strip()
    CreateRepo(
        base_url + "/user/repos",
        {"name": repo_name, "private": private, "description": repo_desc},
        {"Authorization": "token {}".format(token)},
    )
    RevertChanges(username, token, repo_name)


if __name__ == "__main__":
    logging.info("-" * 48)
    logging.info("Create a GitHub repository from the command line")
    logging.info("-" * 48)
    main()
    logging.info("Complete.")

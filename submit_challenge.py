# -*- coding: utf-8 -*-
import requests
import json


def send_challenge():
    url = "https://advana-challenge-check-api-cr-k4hdbggvoq-uc.a.run.app/software-engineer"

    body = {
        "name": "Manuel Cabeza Gallucci",
        "mail": "mcabezag@fi.uba.com",
        "github_url": "https://github.com/manuelcgallucci/LATAM-challenge",
        "api_url": "https://latam-challenge-mcg-1033345485079.us-central1.run.app",
    }

    response = requests.post(url, json=body)

    if response.status_code != 200:
        print("Request failed (sc:", response.status_code, ")")
        return

    print("Submission was successful!")
    print("Response:", response.json())

    with open("submission_response.txt", "w") as f:
        json.dump(response.json(), f, indent=4)


if __name__ == "__main__":
    send_challenge()

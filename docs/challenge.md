

## Part I

### Choosing the model from the DS work

- Fixing exploration.ipynb graphs bugs
- Choosing the model which has better perfomance (balanced and with only top10 features)
- Typically XGBoost is preferable on larger datasets with non-linear and more complex relations (non-linear). In this case some features are correlated so the patterns are better captured by the XGBoost model.

## Writing model class

- Writing model.py, the method _get_min_diff was added from the collab, which should also be tested in test_model.py.
- The preprocessing is done by doing one-hot encoding and taking the top10 features. Targets are calculated the same way as the ipynb.
- The fit is done directly using the features and targets. Here, we asume the train/test split is done somewhere else.

- The model is trained on the data and then exported using xgb to be used in production.
- Load the trained model saved in /models/xgboost_model.json by default. This is done because one test requires the model to be used before fit.
- ! Since it is a small model and a challenge, i have uploaded the model to the repo in /models but this is NOT a good practice. The model should be stored somewhere else outside of the repo, like a cloud bucket for example.

- Added xgboost to requirements and updated some libraries versions

### Possible improvements:

- Test coverage, for example some edge cases that could be tested:
    - Model preprocess with data that has no top10 features

# Part II

## Writing an API

- Using fast API.
- Create the PredictRequest and flights models for data validation in request_models.py
- Tests have been modified to correctly patch the DelayModel class from the challenge.model
- Fix column tests for request not being independently checking the columns

### Possible improvements:

- Testing the new class and files, also, properly mocking the model and asserting DelayModel calls.
- Proper mocking should be done in the test so that the model is not loaded


# Part III

## Deploying the API using GCP

In this case I used a Dockerfile to build the image and deploy using uvicorn.
The dockerfile contains the repo and exposes the port for the API. It can be deployed locally by using:

```bash
sudo docker build -t latam-challenge .
sudo docker run -d -p 8000:8000 latam-challenge
```

To deplot in GCP I use the Google Run, which I can attach to deploy the dockerfile automatically. For this I attach the repo using the Google Run UI. For challenge purposes,the API is left public and without autoscaling.


# Part IV

## CI pipeline

The pipeline for continous integration should run the tests whenever a pr is done to develop or main. It also contains linting and formatting, which should normally run on the pre-commit hook.

## CD pipeline

The pipeline for continous delivery runs when a push is made to the main branch. It was done using the Cloud Run to build the Dockerfile that is defined in the repos root dir (/Dockerfile). The trigger is setup via cloud Build to look for pushes to the main branch. (for challenge purposes I have chosen the yml to be explicitly defined in the repo (GC allows for inline yaml)). The yaml used in GCP is can be found [here](/docs/cloudbuild.yaml)

## Comments on possible improvements to the pipelines:
Extra additions that should be put in place:
- Build an image for testing / pre-commit
- Merging and branching rules for both branches (develop and main). To stop meging commits and only allow prs
- Adding the staging branch for qa (between develop and main)
- Adding a pre-commit hook to the user IDE (pre-commit install)
- Adding environment and github secrets

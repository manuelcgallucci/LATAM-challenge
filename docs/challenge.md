# Part I

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

There are many ways of deploying using GCP, such as using the container registry and deploying with commands directly in the cd.yaml. Also, the model would typically be saved in a google cloud bucket. In this case I used Cloud Build and Cloud Run.

The pipeline for continous delivery runs when a push is made to the main branch. It was done using the Cloud Run to build the Dockerfile that is defined in the repos root dir (/Dockerfile). The trigger is setup via cloud Build to look for pushes to the main branch. The yaml used by GCP once it is all setup can be found [here](/docs/cloudbuild.yaml). This could also be done manually in a cd.yaml.

## Comments on possible improvements to the pipelines:
Extra additions that should be put in place:
- Build an image for testing / pre-commit
- Merging and branching rules for both branches (develop and main). To stop meging commits and only allow prs
- Adding the staging branch for qa (between develop and main)
- Adding a pre-commit hook to the user IDE (pre-commit install)
- Adding environment and github secrets

# Part V (Stress test on API) [Extra]

The Makefile had to be modified so that flask is updated (to 3.1.5). The stress tests where successful, these are the results:

```
[2025-02-12 12:45:26,174] manuel-laptop/INFO/locust.main: Time limit reached. Stopping Locust.
[2025-02-12 12:45:26,176] manuel-laptop/INFO/locust.runners: Stopping 60 users
[2025-02-12 12:45:26,233] manuel-laptop/INFO/locust.runners: 60 Users have been stopped, 0 still running
[2025-02-12 12:45:26,267] manuel-laptop/INFO/locust.main: Running teardowns...
[2025-02-12 12:45:26,267] manuel-laptop/INFO/locust.main: Shutting down (exit code 0), bye.
[2025-02-12 12:45:26,267] manuel-laptop/INFO/locust.main: Cleaning up runner...
 Name                                                          # reqs      # fails  |     Avg     Min     Max  Median  |   req/s failures/s
--------------------------------------------------------------------------------------------------------------------------------------------
 POST /predict                                                   1851     0(0.00%)  |     964     184    2901     750  |   30.92    0.00
--------------------------------------------------------------------------------------------------------------------------------------------
 Aggregated                                                      1851     0(0.00%)  |     964     184    2901     750  |   30.92    0.00

Response time percentiles (approximated)
 Type     Name                                                              50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|------------------------------------------------------------|---------|------|------|------|------|------|------|------|------|------|------|------|
 POST     /predict                                                          750   1100   1300   1600   2200   2600   2700   2800   2900   2900   2900   1851
--------|------------------------------------------------------------|---------|------|------|------|------|------|------|------|------|------|------|------|
 None     Aggregated                                                        750   1100   1300   1600   2200   2600   2700   2800   2900   2900   2900   1851
```

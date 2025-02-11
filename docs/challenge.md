

## Part I

### Choosing the model from the DS work

- Fixing exploration.ipynb graphs bugs
- Choosing the model which has better perfomance (balanced and with only top10 features)
- Typically XGBoost is preferable on larger datasets with non-linear and more complex relations (non-linear). In this case some features are correlated so the patterns are better captured by the XGBoost modle.

## Writing model class

- Writing model.py, the method _get_min_diff was added from the collab, which should also be tested in test_model.py.
- The preprocessing is done by doing one-hot encoding and taking the top10 features. Targets are calculated the same way as the ipynb. 
- The fit is done directly using the features and targets. Here, we asume the train/test split is done somewhere else.

# Part II

## Writing an API

- Using fast API.
- Create the PredictRequest and flights models for data validation
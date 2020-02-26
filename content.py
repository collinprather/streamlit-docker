"""
Contains all raw text for the web app.
Keeping in a separate file keeps app.py cleaner.
"""

intro = """This web app is designed to show how one can simply deploy a machine learning model. 
A web app like this could enable non-technical employees to easily leverage the model's predictions in their work, 
or explain the logic behind the model's predictions. For this example, we'll be using the famous [Boston housing dataset](https://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html),
 as provided by `scikit-learn`."""

model_explanation = """Let's assume that we are using a simple decision tree to estimate how we should value a new house that hits the market.
We'll restrain our tree to have a `max_depth` of 2. After fitting the tree, it is relatively easy to make predictions about new houses, but what is often more
important to stakeholders is *why* the model makes its predictions. The good news for us is that decision trees lend themselves particularly well to visual interpretation.
In fact, using the [`dtreeviz`](https://github.com/parrt/dtreeviz) package, we can generate a nice svg that even highlights the path that a particular observation takes down
the tree."""

slider_explanation = """Since we know that our decision tree identified the `RM` and `LSTAT` features as most important to predicting the house price,
we can allow the user to input their own values for these two features and observe how the model's predictions change."""

# prediction_explanation =
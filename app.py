import streamlit as st
import numpy as np
from dtreeviz.trees import *
from sklearn.datasets import load_boston
from sklearn.tree import DecisionTreeRegressor
import base64


# @st.cache()
# don't cache here, but may want to reference in article
@st.cache()
def load_data():
    boston = load_boston()
    X = boston.data
    y = boston.target * 10_000
    feature_names = boston.feature_names
    return X, y, feature_names

@st.cache()
def fit_dtree(X, y):
    """
    in a realistic setting, probably train model elsewhere, then load it..
    """
    dtree = DecisionTreeRegressor(max_depth=2)
    dtree.fit(X, y)
    return dtree

# https://gist.github.com/treuille/8b9cbfec270f7cda44c5fc398361b3b1
def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)



if __name__ == "__main__":
    ### loading things up
    text = st.sidebar.title("Built on:")
    logo = st.sidebar.image("images/aws.png")
    logo = st.sidebar.image("images/docker.png")

    title = st.title("Explainable ML")

    intro = st.markdown("""This web app is designed to show how one can simply deploy a machine learning model. 
A web app like this could enable non-technical employees to easily leverage the model's predictions in their work, 
or explain the logic behind the model's predictions. For this example, we'll be using the famous [Boston housing dataset](https://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html),
 as provided by `scikit-learn`. 
                        
                        """)

    model_explanation = st.markdown("""
Let's assume that we are using a simple decision tree to estimate how we should value a new house that hits the market.
We'll restrain our tree to have a `max_depth` of 2. After fitting the tree, it is relatively easy to make predictions about new houses, but what is often more
important to stakeholders is *why* the model makes its predictions. The good news for us is that decision trees lend themselves particularly well to visual interpretation.
In fact, using the [`dtreeviz`](https://github.com/parrt/dtreeviz) package, we can generate a nice svg that even highlights the path that a particular observation takes down
the tree.
    """)

    slider_explanation = st.markdown("""
Since we know that our decision tree identified the `RM` and `LSTAT` features as most important to predicting the house price,
we can allow the user to input their own values for these two features and observe how the model's predictions change.
        """)

    # fitting models
    X, y, feature_names = load_data()
    dtree = fit_dtree(X, y)

    # sliders for new predictions
    RM = st.slider("RM: average number of rooms per dwelling.",
                         min_value=3.6,
                         max_value=8.7,
                         value=6.0,
                         step=.1)
    LSTAT = st.slider("LSTAT: percentage of the population denoted as lower status.",
                         min_value=2.0,
                         max_value=37.0,
                         value=14.0,
                         step=.1)
    new_observation = np.array([0, 0, 0, 0, 0, RM, 0, 0, 0, 0, 0, 0, LSTAT])

    # viz the predictions path
    viz = dtreeviz(dtree,
               X, 
               y, 
               target_name='price', 
               orientation ='LR',  # left-right orientation
               feature_names=feature_names,
               X=new_observation)  # need to give single observation for prediction
              
    viz.save("images/prediction_path.svg")
    
    with open("images/prediction_path.svg", "r") as f:
        svg = f.read()
    
    render_svg(svg)

    prediction_explanation = st.markdown(f"""
According to the model, a house with {round(RM, 1)} rooms located in a neighborhood that is {LSTAT/100:.1%} lower status 
should be valued at approximately ${dtree.predict(new_observation.reshape(1, -1)).item():,.0f}.
        """)

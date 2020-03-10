# local
import content

# 3rd party
import streamlit as st
import numpy as np
from dtreeviz.trees import *
from sklearn.datasets import load_boston
from sklearn.tree import DecisionTreeRegressor

# built-in
import base64

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
    With bigger data, or a more complex model,
    you'd probably want to train offline, then
    load into app.
    """
    dtree = DecisionTreeRegressor(max_depth=2)
    dtree.fit(X, y)
    return dtree

def render_svg(svg):
    """
    Renders the given svg string.
    https://gist.github.com/treuille/8b9cbfec270f7cda44c5fc398361b3b1
    """
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)



if __name__ == "__main__":
    ### loading things up
    text = st.sidebar.title("Built on:")
    # logo = st.sidebar.image("images/streamlit.png")
    logo = st.sidebar.image("images/aws.png")
    logo = st.sidebar.image("images/docker.png")

    # text content
    title = st.title("Explainable ML")
    intro = st.markdown(content.intro)
    model_explanation = st.markdown(content.model_explanation)
    slider_explanation = st.markdown(content.slider_explanation)

    # fitting model
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

    # read in svg prediction path and display
    with open("images/prediction_path.svg", "r") as f:
        svg = f.read()
    render_svg(svg)
    prediction_explanation = st.markdown(f"""According to the model, a house with {round(RM, 1)} rooms located in a neighborhood that is {LSTAT/100:.1%} lower status 
should be valued at approximately ${dtree.predict(new_observation.reshape(1, -1)).item():,.0f}.""")

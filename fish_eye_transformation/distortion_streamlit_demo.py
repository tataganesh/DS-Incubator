import numpy as np
import streamlit as st
from transformations import applyFisheye, applyBarrelDistorion
from PIL import Image

# Interactive Streamlit elements, like these sliders, return their value.
# This gives you an extremely simple interaction model.
def skimage_sidebar():
    r1 = st.sidebar.slider("r1", 0.0, 1.0, 0.8)
    r2 = st.sidebar.slider("r2", 1.0, 3.0, 2.1)
    r3 = st.sidebar.slider("r3", 1.0, 3.0, 1.8)
    return r1, r2, r3

def barrelTransform_sidebar():
    k = st.sidebar.slider('k', -10, 10, 1)
    dx = st.sidebar.slider('dx', -50, 50, 0)
    dy = st.sidebar.slider('dy', -50, 50, 0)
    return k, dx, dy

img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
genre = st.radio("Transformation options", ("Skimage", "Barrel transform"))


if img_file_buffer is not None:
    inputImage = np.array(Image.open(img_file_buffer))
    if genre == "Skimage":
        r1, r2, r3 = skimage_sidebar()
        fishEyeOutput = applyFisheye(inputImage, r1, r2, r3)
    elif genre == "Barrel transform":
        k, dx, dy = barrelTransform_sidebar()
        fishEyeOutput = applyBarrelDistorion(inputImage, k, dx, dy)

    inputImagePl = st.empty()
    image = st.empty()

    # Update the image placeholder by calling the image() function on it.
    image.image(fishEyeOutput, use_column_width=False)
    inputImagePl.image(inputImage, use_column_width=False)
st.button("Re-run")
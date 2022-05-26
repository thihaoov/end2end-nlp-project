import streamlit as st

# EDA pkgs
import pandas as pd
import numpy as np
import altair as alt

# Utils
import joblib

pipe_lr = joblib.load(open("models/emotion_classifier_pipe_lr_24_may_2022.pkl", 'rb'))

# Fxn
def predict_emotions(docx):
    result = pipe_lr.predict([docx])
    return result

def get_prediction_prob(docx):
    result = pipe_lr.predict_proba([docx])
    return result

emotions_emoji_dict = {"anger":"😠","disgust":"🤮", "fear":"😨😱", "happy":"🤗", "joy":"😂", "neutral":"😐", "sad":"😔", "sadness":"😔", "shame":"😳", "surprise":"😮"}

def main():
    st.title("Emotion Classifier App")
    menu = ["Home", "Monitor", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home-Emotion in Text")
        with st.form(key="emotion_clf_form"):
            raw_text = st.text_area("Type here")
            submit_text = st.form_submit_button(label="Submit")
        if submit_text:
            col1, col2 = st.columns(2)

            #Apply Fxn Here
            prediction = predict_emotions(raw_text)
            probability = get_prediction_prob(raw_text)

            with col1:
                st.success("Original Text")
                st.write(raw_text)

                st.success("Prediction")
                emoji_icon = emotions_emoji_dict[prediction[0]]
                st.write("{} : {}".format(prediction[0], emoji_icon))
                st.write("Confidence:{}".format(np.max(probability)))
            with col2:
                st.success("Prediction Probability")
                # st.write(probability)
                proba_df = pd.DataFrame(probability, columns=pipe_lr.classes_)
                # st.write(proba_df.T)
                proba_df_clean = proba_df.T.reset_index()
                proba_df_clean.columns = ["emotions", "probability"]

                fig = alt.Chart(proba_df_clean).mark_bar().encode(x='emotions', y='probability', color='emotions')
                st.altair_chart(fig, use_container_width=True)


    elif choice == "Monitor":
        st.subheader("Monitor App")


if __name__ == '__main__':
    main()
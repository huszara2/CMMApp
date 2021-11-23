import streamlit as st
import numpy as np
import pickle
from sklearn.tree import DecisionTreeClassifier

#model = DecisionTreeClassifier(max_depth=8)

model = pickle.load(open('model.pickle','rb'))


st.write("""
# CoverMyMeds - PA Approval Chances
""")

st.write("This project was done as part of the Erdos Data Science bootcamp Fall 2021. The data was provided by CoverMyMeds.")

st.header("User Information")

st.write("Please fill in the following information." )

bin = st.radio("Select the BIN of Insurance payer: ", ("417380","417614","417740","999001"))

drug = st.radio("Select the drug that you want covered: ", ("A","B","C"))

tried_failed = st.radio("Have you tried and failed the generic alternative?", ("Yes","No"))

contraindication = st.radio("Do you have an associated contraindication for the medication requested (i.e. is there any reason you cannot take this drug)?",("Yes","No"));

correct_diagnosis = st.radio("Do you have the corrected diagnosis for the associated drug?",("Yes","No"));


# Find reject code:
reject_code = 0;
if bin == "417380":
    if drug == "A":
        reject_code = 75;
    elif drug == "B":
        reject_code = 76;
    elif drug == "C":
        reject_code = 70;
elif bin == "417614":
    if drug == "A":
        reject_code = 70;
    elif drug == "B":
        reject_code = 75;
    elif drug == "C":
        reject_code = 76;
elif bin == "417740":
    if drug == "A":
        reject_code = 76;
    elif drug == "B":
        reject_code = 70;
    elif drug == "C":
        reject_code = 75;
elif bin == "999001":
    reject_code = 76;

#Set features
d = {"Yes":1, "No":0} #Dictionary for Yes = 1, No  = 0

cd = d[correct_diagnosis]
tf = d[tried_failed]
contra = d[contraindication]
drug_B = int(drug == "B")
drug_C = int(drug == "C")
bin_417614 = int(bin == "417614")
bin_417740 = int(bin == "417740")
bin_999001 = int(bin == "999001")
reject_code_75 = int(reject_code == 75)
reject_code_76 = int(reject_code == 76)

#Predict
pred = model.predict_proba([[cd,tf,contra,drug_B,drug_C,bin_417614,bin_417740,bin_999001, reject_code_75, reject_code_76]])

if tf == 0:
    pred1 = model.predict_proba([[cd,1,contra,drug_B,drug_C,bin_417614,bin_417740,bin_999001, reject_code_75, reject_code_76]])

st.header("Result")
st.write("""The chances of your PA being approved are: **{}**""".format(np.round(100*pred[0,1],3)), "%.")

if tf == 0:
    st.write("""In addition, if you first try the generic alternative but still need this drug, then the chances of your PA form being approved are: {}""".format(np.round(100*pred1[0,1],3)), "%.")

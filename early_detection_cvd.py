#TODO change person_index system
"""
Clinical Decision Support for Early Detection of CVD

This system uses guidelines outlined in Cohn et al., 2003 to screen
individuals for asymptomatic CVD.
"""
from owlready2 import *

import numpy as np
import pandas as pd
import os


def get_pulse_contour_analysis_result(person, cvd_assessment):
    if person.age <= 45:
        if person.sex == "male":
            if cvd_assessment.pulseContourAnalysis >= 15:
                result = "normal"
            elif cvd_assessment.pulseContourAnalysis >= 12 and cvd_assessment.pulseContourAnalysis <= 14.9:
                result = "borderline"
            else:
                result = "abnormal"
        else:
            if cvd_assessment.pulseContourAnalysis >= 12:
                result = "normal"
            elif cvd_assessment.pulseContourAnalysis >= 10 and cvd_assessment.pulseContourAnalysis <= 11.9:
                result = "borderline"
            else:
                result = "abnormal"
    if person.age >= 46 and person.age <= 64:
        if person.sex == "male":
            if cvd_assessment.pulseContourAnalysis >= 12:
                result = "normal"
            elif cvd_assessment.pulseContourAnalysis >= 10 and cvd_assessment.pulseContourAnalysis <= 11.9:
                result = "borderline"
            else:
                result = "abnormal"
        else:
            if cvd_assessment.pulseContourAnalysis >= 10:
                result = "normal"
            elif cvd_assessment.pulseContourAnalysis >= 9 and cvd_assessment.pulseContourAnalysis <= 9.9:
                result = "borderline"
            else:
                result = "abnormal"
    if person.age >= 65:
        if person.sex == "male":
            if cvd_assessment.pulseContourAnalysis >= 10:
                result = "normal"
            elif cvd_assessment.pulseContourAnalysis >= 9 and cvd_assessment.pulseContourAnalysis <= 9.9:
                result = "borderline"
            else:
                result = "abnormal"
        else:
            if cvd_assessment.pulseContourAnalysis >= 9:
                result = "normal"
            elif cvd_assessment.pulseContourAnalysis >= 8 and cvd_assessment.pulseContourAnalysis <= 8.9:
                result = "borderline"
            else:
                result = "abnormal"
    return result


def get_resting_blood_pressure_result(cvd_assessment):
    if cvd_assessment.restingBloodPressure[0] < 130 and cvd_assessment.restingBloodPressure[1] < 85:
        return "normal"
    elif cvd_assessment.restingBloodPressure[0] >= 140 or cvd_assessment.restingBloodPressure[1] >= 90:
        return "abnormal"
    else:
        return "borderline"


def get_exercise_blood_pressure_result(cvd_assessment):
    if cvd_assessment.exerciseBloodPressure < 30:
        return "normal"
    elif cvd_assessment.exerciseBloodPressure >= 40:
        return "abnormal"
    else:
        return "borderline"


def get_optic_fundus_result(cvd_assessment):
    if cvd_assessment.opticFundus > 3.5:
        return "normal"
    elif cvd_assessment.opticFundus <= 1.2:
        return "abnormal"
    else:
        return "borderline"


def get_microalbuminaria_result(cvd_assessment):
    if cvd_assessment.Microalbuminuria <= 0.6:
        return "normal"
    elif cvd_assessment.Microalbuminuria >= 1:
        return "abnormal"
    else:
        return "borderline"


def get_electrocardiogram_result(cvd_assessment):
    if cvd_assessment.Electrocardiogram == "none":
        return "normal"
    elif cvd_assessment.Electrocardiogram == "diagnostic":
        return "abnormal"
    else:
        return "borderline"


def get_lv_ultrasound_result(cvd_assessment):
    if cvd_assessment.LVUltrasound < 2.7:
        return "normal"
    elif cvd_assessment.LVUltrasound >= 2.9:
        return "abnormal"
    else:
        return "borderline"


def get_bnp_result(cvd_assessment):
    if cvd_assessment.BNP <= 50:
        return "normal"
    elif cvd_assessment.BNP >= 100:
        return "abnormal"
    else:
        return "borderline"


def get_smoking_recommendation(person, treatment_recommendation):
    if person.isSmoker:
        treatment_recommendation.quitSmoking = True
        print(
            "This patient should strongly consider quitting smoking. Please "
            "discuss options to support patient in this endeavor."
        )


def get_arterial_elasticity_recommendation(
    person,
    cvd_assessment,
    treatment_recommendation
):
    arterial_elasticity_results = []
    pulse_contour_analysis_result = arterial_elasticity_results.append(get_pulse_contour_analysis_result(person, cvd_assessment))
    resting_bp_result = arterial_elasticity_results.append(get_resting_blood_pressure_result(cvd_assessment))
    exercise_bp_result = arterial_elasticity_results.append(get_exercise_blood_pressure_result(cvd_assessment))
    if "abnormal" in arterial_elasticity_results:
        arterial_elasticity = "abnormal"
        treatment_recommendation.Nebivol = True
        treatment = "Nebivol should be considered for this patient."
    elif "borderline" in arterial_elasticity_results:
        arterial_elasticity = "borderline"
        treatment_recommendation.Nebivol = True
        treatment = "Nebivol should be considered for this patient."
    else:
        treatment_recommendation.Nebivol = False
        treatment = "No arterial elasticity treatment is needed at this time."
    print("This patient's arterial elasticity is", arterial_elasticity+".", treatment)


def get_cholesterol_recommendation(
    person,
    treatment_assessment,
    treatment_recommendation
):
    if treatment_assessment.LDLCholesterol <= 100:
        ldl = "optimal"
        treatment_recommendation.Statins = False
        treatment = "No cholesterol treatment is needed at this time."
    elif treatment_assessment.LDLCholesterol >= 130:
        ldl = "abnormal"
        treatment_recommendation.Statins = True
        treatment = "Statins are recommended for this patient."
    else:
        ldl = "borderline"
        treatment_recommendation.Statins = True
        treatment = "Discuss possible statin use with patient."
    print("This patient's LDL cholesterol is", ldl+".", treatment)


def get_c_reactive_protein_recommendation(
    person,
    treatment_assessment,
    treatment_recommendation
):
    if treatment_assessment.cReactiveProtein > 0.300:
        result = "abnormal"
        treatment_recommendation.antiInflammatoryTherapy = True
        treatment = "Anti-inflammatory therapy is recommended for this patient."
    else:
        result = "optimal"
        treatment_recommendation.antiInflammatoryTherapy = False
        treatment = "No treatment is recommended at this time."
    print("This patient's C-reactive protein levels are", result+".", treatment)


def get_homocysteine_recommendation(
    person,
    treatment_assessment,
    treatment_recommendation
):
    if treatment_assessment.Homocysteine <= 10:
        result = "optimal"
        treatment_recommendation.folicAcid = False
        treatment = "No treatment is recommended at this time."
    elif treatment_assessment.Homocysteine > 12:
        result = "abnormal"
        treatment_recommendation.folicAcid = True
        treatment = "Folic acid is recommended for this patient."
    else:
        result = "borderline"
        treatment_recommendation.folicAcid = True
        treatment = "Discuss possible folic acid use with patient."
    print("This patient's homocysteine levels are", result+".", treatment)


def get_pai1_recommendation(
    person,
    treatment_assessment,
    treatment_recommendation
):
    if treatment_assessment.plasminogenActivatorInhibitor1 <= 43:
        result = "optimal"
        treatment_recommendation.PAI1Therapy = False
        treatment = "No treatment is recommended at this time."
    else:
        result = "abnormal"
        treatment_recommendation.PAI1Therapy = True
        treatment = "PAI-1 therapy is recommended for this patient."
    print(
        "This patient's plasminogen activator inhibitor 1 levels are",
        result+".", treatment
    )


def evaluate_risk(onto, person):
    if person.age > 44 and person.sex == "male":
        person.is_a.append(onto.highRiskAge)
    if person.cvdPrimaryRelative > 0 or person.cvdSecondaryRelative > 1:
        person.is_a.append(onto.highRiskFamilyHistory)
    if person.hasPersonalHistory:
        person.is_a.append(onto.highRiskPersonalHistory)
    if person.isSmoker:
        person.is_a.append(onto.highRiskSmoker)
    if len(person.is_a) > 1:
        person.is_a.append(onto.HighRiskCVD)


def screen_person(onto, person, person_index):
    screening_file_path = input(
        "This person is considered high risk for CVD. Please order the following"
        " tests: \n"
        "1. Pulse Contour Analysis \n"
        "2. Resting and Exercise Blood Pressure \n"
        "3. BNP \n"
        "4. Electrocardiogram \n"
        "5. LV Ultrasound \n"
        "6. Microalbuminaria \n"
        "7. Optic Fundus \n"
        "Once you have the results, please provide the file path here: "
    )
    # screening_file_path = "/Users/ashish/Desktop/BMI210/project/test_screen_data.csv"
    screening_data = pd.read_csv(os.path.join(os.getcwd(), screening_file_path))
    onto_person_index = person_index + 1
    cvd_assessment = onto.cvdAssessment(
        onto_person_index,
        pulseContourAnalysis = screening_data.iloc[person_index]["pulse_contour_analysis"],
        restingBloodPressure = [screening_data.iloc[person_index]["resting_blood_pressure_sbp"], screening_data.iloc[person_index]["resting_blood_pressure_dbp"]],
        exerciseBloodPressure = screening_data.iloc[person_index]["exercise_blood_pressure_sbp_rise"],
        BNP = screening_data.iloc[person_index]["bnp"],
        Electrocardiogram = screening_data.iloc[person_index]["electrocardiogram_abnormalities"],
        LVUltrasound = screening_data.iloc[person_index]["lv_ultrasound"],
        Microalbuminuria = screening_data.iloc[person_index]["microalbuminuria"],
        opticFundus = screening_data.iloc[person_index]["optic_fundus"]
    )
    scoring = {"normal":0, "borderline":1, "abnormal":2}
    scores = []
    scores.append(scoring[get_pulse_contour_analysis_result(person, cvd_assessment)])
    scores.append(scoring[get_resting_blood_pressure_result(cvd_assessment)])
    scores.append(scoring[get_exercise_blood_pressure_result(cvd_assessment)])
    scores.append(scoring[get_optic_fundus_result(cvd_assessment)])
    scores.append(scoring[get_microalbuminaria_result(cvd_assessment)])
    scores.append(scoring[get_electrocardiogram_result(cvd_assessment)])
    scores.append(scoring[get_lv_ultrasound_result(cvd_assessment)])
    scores.append(scoring[get_bnp_result(cvd_assessment)])
    total_score = sum(scores)
    return [cvd_assessment, (True if total_score >= 5 else False)]


def recommend_treatment(onto, person, person_index, cvd_assessment):
    labs_file_path = input(
        "CVD has been detected in this patient. \n"
        "Please order the following labs to guide treatment. "
        "Once you have the results, please provide the file path here: "
    )
    # labs_file_path = "/Users/ashish/Desktop/BMI210/project/test_labs_data.csv"
    labs_data = pd.read_csv(os.path.join(os.getcwd(), labs_file_path))
    onto_person_index = person_index + 1
    treatment_assessment = onto.treatmentAssessment(
        onto_person_index,
        HDLCholesterol = labs_data.iloc[person_index]["hdl_cholesterol"],
        LDLCholesterol = labs_data.iloc[person_index]["ldl_cholesterol"],
        cReactiveProtein = labs_data.iloc[person_index]["c_reactive_protein"],
        Glucose = labs_data.iloc[person_index]["glucose"],
        Homocysteine = labs_data.iloc[person_index]["homocysteine"],
        plasminogenActivatorInhibitor1 = labs_data.iloc[person_index]["pai1"],
        Triglycerides = labs_data.iloc[person_index]["triglycerides"]
    )
    # TODO add treatments to ontology
    treatment_recommendation = onto.Treatment(
        onto_person_index
    )
    get_smoking_recommendation(person, treatment_recommendation)
    get_arterial_elasticity_recommendation(person, cvd_assessment, treatment_recommendation)
    get_cholesterol_recommendation(person, treatment_assessment, treatment_recommendation)
    get_c_reactive_protein_recommendation(person, treatment_assessment, treatment_recommendation)
    get_homocysteine_recommendation(person, treatment_assessment, treatment_recommendation)
    get_pai1_recommendation(person, treatment_assessment, treatment_recommendation)

def main():
    onto = get_ontology("file://cvd_early_detection.owl").load()
    risk_factor_file_path = input(
        "Welcome to the CVD Early Detection Screen. Let's begin. \n "
        "Does this patient have any CVD risk factors? (Please provide a csv file "
        "path with this patient's CVD risk factors): "
    )
    # risk_factor_file_path = "/Users/ashish/Desktop/BMI210/project/test_data.csv"
    risk_factor_data = pd.read_csv(os.path.join(os.getcwd(), risk_factor_file_path))
    for person_index in risk_factor_data.index:
        onto_person_index = person_index + 1
        person = onto.Person(
            onto_person_index,
            age = int(risk_factor_data.iloc[person_index]["age"]),
            sex = risk_factor_data.iloc[person_index]["sex"],
            cvdPrimaryRelative = int(risk_factor_data.iloc[person_index]["primary_relative_with_cvd"]),
            cvdSecondaryRelative = int(risk_factor_data.iloc[person_index]["secondary_relative_with_cvd"]),
            hasDiabetes = bool(risk_factor_data.iloc[person_index]["has_diabetes"]),
            hasPersonalHistory = bool(risk_factor_data.iloc[person_index]["has_personal_history"]),
            isSmoker = bool(risk_factor_data.iloc[person_index]["is_smoker"])
        )
        evaluate_risk(onto, person)
        if onto.HighRiskCVD in person.is_a:
            cvd_assessment, disease_present = screen_person(onto, person, person_index)
            if disease_present or person.hasDiabetes:
                recommend_treatment(onto, person, person_index, cvd_assessment)


if __name__ == "__main__":
    main()

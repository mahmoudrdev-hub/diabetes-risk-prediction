import pandas as pd


def add_engineered_features(data):
    data = data.copy()

    data["CardioMetabolicRisk"] = (
        data["HighBP"]
        + data["HighChol"]
        + data["HeartDiseaseorAttack"]
        + data["Stroke"]
    )

    data["LifestyleRisk"] = (
        data["Smoker"]
        + (1 - data["PhysActivity"])
        + (1 - data["Fruits"])
        + (1 - data["Veggies"])
        + data["HvyAlcoholConsump"]
    )

    data["HealthcareAccessRisk"] = (1 - data["AnyHealthcare"]) + data["NoDocbcCost"]

    data["HealthBurden"] = (
        data["GenHlth"] + data["MentHlth"] + data["PhysHlth"] + data["DiffWalk"]
    )

    data["SocioEconomicScore"] = data["Education"] + data["Income"]

    data["BMI_Category"] = pd.cut(
        data["BMI"],
        bins=[0, 18.5, 25, 30, 100],
        labels=[0, 1, 2, 3],
    ).astype(int)

    return data

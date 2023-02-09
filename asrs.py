import json
import numpy as np

def getAsrsVector(asrs_df):
    questions = []
    questions.append(asrs_df[(asrs_df.name.str.contains('1_0'))].responses)
    questions.append(asrs_df[(asrs_df.name.str.contains('1_3'))].responses)
    questions.append(asrs_df[(asrs_df.name.str.contains('2_0'))].responses)
    questions.append(asrs_df[(asrs_df.name.str.contains('2_3'))].responses)
    questions.append(asrs_df[(asrs_df.name.str.contains('2_6'))].responses)
    questions.append(asrs_df[(asrs_df.name.str.contains('2_9'))].responses)
    
    vector = np.array([])
    for question in questions:
        obj = json.loads(question.iloc[0])
        q1 = obj.get('Q0')
        q2 = obj.get('Q1')
        q3 = obj.get('Q2')
        vector = np.append(vector, [q1, q2, q3])    
        
    return vector
    
def getAsrsResults(single_df):
    asrs_df = single_df[~single_df.name.isna()]
    asrs_df = asrs_df[(asrs_df.name.str.contains('ASRS'))].responses
    
    obj = json.loads(asrs_df.iloc[0])
    asrs_1 = obj.get('Q0')
    asrs_2 = obj.get('Q1')
    asrs_3 = obj.get('Q2')

    obj = json.loads(asrs_df.iloc[1])
    asrs_4 = obj.get('Q0')
    asrs_5 = obj.get('Q1')
    asrs_6 = obj.get('Q2')

    obj = json.loads(asrs_df.iloc[2])
    asrs_7 = obj.get('Q0')
    asrs_8 = obj.get('Q1')
    asrs_9 = obj.get('Q2')

    obj = json.loads(asrs_df.iloc[3])
    asrs_10 = obj.get('Q0')
    asrs_11 = obj.get('Q1')
    asrs_12 = obj.get('Q2')

    obj = json.loads(asrs_df.iloc[4])
    asrs_13 = obj.get('Q0')
    asrs_14 = obj.get('Q1')
    asrs_15 = obj.get('Q2')

    obj = json.loads(asrs_df.iloc[5])
    asrs_16 = obj.get('Q0')
    asrs_17 = obj.get('Q1')
    asrs_18 = obj.get('Q2')

    sum_part_one = asrs_1 + asrs_2 + asrs_3 + asrs_4 + asrs_5 + asrs_6
    sum_part_two = asrs_7 + asrs_8 + asrs_9 + asrs_10 + asrs_11 + \
        asrs_12 + asrs_13 + asrs_14 + asrs_15 + asrs_16 + asrs_17 + asrs_18

    # asrs_vector = getAsrsVector(asrs_df)
    return [sum_part_one, sum_part_two]
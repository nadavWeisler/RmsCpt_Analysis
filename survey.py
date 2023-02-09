import json
    
def getSurveyResultsByTrialIndex(df, trialIndex):
    q_df = df[df.trial_index == trialIndex].responses
    return getSurveyResults(q_df)

def getSurveyResultsByBlock(df, block):
    q_df = df[df.stimulus_block == block].responses
    return getSurveyResults(q_df)

def getSurveyResults(q_df):
    q_obj = json.loads(q_df.iloc[0])
    q0, q1, q2 = None, None, None
    try:
        q0 = q_obj.get('Q0')
        q1 = q_obj.get('Q1')
        q2 = q_obj.get('Q2')
    finally:
        if q1 is None:
            return [q0]
        elif q2 is None:
            return [q0, q1]
        else: 
            return [q0, q1, q2]    
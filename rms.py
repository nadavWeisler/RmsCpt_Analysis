from utils import getStandartRt


def get_only_correct(brms_df):
    if "correct" in brms_df:
        return brms_df[brms_df.correct == True]
    else:
        return brms_df[((brms_df.key_press == 'P') & (brms_df.stimulus_side == 0)) | (
            (brms_df.key_press == 'Q') & (brms_df.stimulus_side == 1))]


def getRmsResults(df, sd=2.5, min_rt=200, max_rt=8000):
    rms_df = df[(df.trial_type == 'bRMS')]
    rms_df = rms_df[rms_df.stimulus_block != 'training']
    rms_df = rms_df[rms_df.stimulus_block != 'control']
    rms_df = rms_df[(rms_df.rt > min_rt) & (rms_df.rt < max_rt)]
    rms_correct = get_only_correct(rms_df)
    if rms_correct.shape[0] or rms_df.shape[0] == 0:
        return 0, 0, 1
    error_percent = (rms_df.shape[0] - rms_correct.shape[0]) / rms_df.shape[0]
    rms_standard = getStandartRt(rms_correct, sd)
    return rms_standard.rt.mean(), rms_standard.rt.std(), error_percent


def getFaceInversionEffect(rms_df):
    regular_f_brms = rms_df[(rms_df.stimulus_block == "main")]
    reverted_f_brms = rms_df[(rms_df.stimulus_block == "reversed")]
    if regular_f_brms.shape[0] == 0 or reverted_f_brms.shape[0] == 0:
        return None
    else:
        return reverted_f_brms.rt.mean() - regular_f_brms.rt.mean()

def getNullAnswer(control_exist=False):
    if control_exist:
        return [0, 0, 1, 0, 0, 0, 1, 0]
    else:
        return [0, 0, 1, 0]

def getDetaliedRMSResult(df, sd=2.5, control_exist=False):
    rms_df = df[(df.trial_type == 'bRMS')]
    rms_df = rms_df[rms_df.stimulus_block != 'training']

    if control_exist:
        rms_control_df = rms_df[rms_df.stimulus_block.str.contains('control')]
        rms_control_df = rms_control_df[rms_control_df.rt > 200]
        rms_control_df = rms_control_df[rms_control_df.rt < 8000]
        rms_control_correct = get_only_correct(rms_control_df)
        error_percent_control = (
            (rms_control_df.shape[0] - rms_control_correct.shape[0]) / rms_control_df.shape[0])
        rms_control_standard = getStandartRt(rms_control_correct, sd)
        control_face_invertion_effect = getFaceInversionEffect(rms_control_standard)

    rms_df = rms_df[~rms_df["stimulus_block"].str.contains(
        'control', na=False)]
    rms_df = rms_df[(rms_df.rt > 200) & (rms_df.rt < 8000)]
    if rms_df.shape[0] == 0:
        return getNullAnswer(control_exist)
    rms_correct = get_only_correct(rms_df)
    if rms_correct.shape[0] == 0:
        return getNullAnswer(control_exist)
    error_percent = (rms_df.shape[0] - rms_correct.shape[0]) / rms_df.shape[0]
    rms_standard = getStandartRt(rms_correct, sd)
    face_invertion_effect = getFaceInversionEffect(rms_standard)

    results = [rms_standard.rt.mean(), rms_standard.rt.std(),
               error_percent, face_invertion_effect]
    
    if control_exist:
        results.extend([rms_control_standard.rt.mean(), rms_control_standard.rt.std(
        ), error_percent_control, control_face_invertion_effect])

    return results

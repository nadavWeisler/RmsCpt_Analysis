from utils import getStandartRt


def getCptResults(single_df, numOfSd=3):
    cpt_df = single_df[single_df.trial_type == 'image-cpt']
    cpt_df = cpt_df[cpt_df.stimulus_block != 'training']
    errors = len(cpt_df[((cpt_df.key_press == '32') & (cpt_df.is_stimulus == False)) |
                        ((cpt_df.key_press != '32') & (cpt_df.is_stimulus == True))])
    correct_cpt = cpt_df[((cpt_df.key_press == "32") &
                          (cpt_df.is_stimulus == True))]
    correct_cpt = correct_cpt[correct_cpt.rt > 150]
    correct_cpt = correct_cpt[correct_cpt.rt < 3000]
    standard_cpt = getStandartRt(correct_cpt, numOfSd)
    return standard_cpt.rt.mean(), standard_cpt.rt.std(), errors
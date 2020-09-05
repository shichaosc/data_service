'''
1	听力	国际版
2	发音	国际版
3	词汇	国际版
4	拼音识读	国际版
5	表达与运用	国际版
6	听力	高级版
7	拼音	高级版
8	识字	高级版
9	语音积累	高级版
10	语音运用	高级版
'''

SUBJECT_ID_INFO = {
    '1': {'apply_level': 1, 'ability_id': [1]},
    '2': {'apply_level': 1, 'ability_id': [1]},
    '3': {'apply_level': 1, 'ability_id': [1, 3]},
    '4': {'apply_level': 1, 'ability_id': [1, 3]},
    '5': {'apply_level': 1, 'ability_id': [1, 3]},
    '6': {'apply_level': 1, 'ability_id': [1, 3]},
    '7': {'apply_level': 1, 'ability_id': [2]},
    '8': {'apply_level': 1, 'ability_id': [2]},
    '9': {'apply_level': 1, 'ability_id': [2, 5]},
    '10': {'apply_level': 1, 'ability_id': [2, 5]},
    '11': {'apply_level': 1, 'ability_id': [2, 5]},
    '12': {'apply_level': 1, 'ability_id': [2, 5]},
    '13': {'apply_level': 1, 'ability_id': [4]},
    '14': {'apply_level': 1, 'ability_id': [4]},
    '15': {'apply_level': 1, 'ability_id': [4]},

    '16': {'apply_level': 1, 'ability_id': [6]},
    '17': {'apply_level': 1, 'ability_id': [6]},
    '18': {'apply_level': 2, 'ability_id': [6]},
    '19': {'apply_level': 1, 'ability_id': [7]},
    '20': {'apply_level': 1, 'ability_id': [7]},
    '21': {'apply_level': 2, 'ability_id': [1]},
    '22': {'apply_level': 1, 'ability_id': [1]},
    '23': {'apply_level': 2, 'ability_id': [8]},
    '24': {'apply_level': 2, 'ability_id': [8]},
    '25': {'apply_level': 1, 'ability_id': [9]},
    '26': {'apply_level': 2, 'ability_id': [9]},
    '27': {'apply_level': 2, 'ability_id': [9]},
    '28': {'apply_level': 1, 'ability_id': [9]},
    '29': {'apply_level': 1, 'ability_id': [9]},
    '30': {'apply_level': 2, 'ability_id': [9]},
    '31': {'apply_level': 1, 'ability_id': [10]},
    '32': {'apply_level': 2, 'ability_id': [10]},
    '33': {'apply_level': 2, 'ability_id': [10]},
    '34': {'apply_level': 1, 'ability_id': [10]},
    '35': {'apply_level': 2, 'ability_id': [10]}
}


def subject_id_select(last_subject, second_last_subject):
    subject_id = last_subject[0]
    switch = {
        '2': subject_2,
        '17': subject_17,
        '20': subject_20,
        '23': subject_23,
        '26': subject_26,
        '29': subject_29,
        '32': subject_32
    }

    return switch.get(subject_id)(last_subject, second_last_subject)

def subject_2(last_subject, second_last_subject):
    '''前两道题有都答对走高级版，不然走国际版'''

    if last_subject[1] == '1' and second_last_subject[1] == '1':
        next_question_ids = [16, 17]
    else:
        next_question_ids = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    return next_question_ids

def subject_17(last_subject, second_last_subject):
    if last_subject[1] == '1' and second_last_subject[1] == '1':
        next_question_ids = [18, 19, 20]
    else:
        next_question_ids = [19, 20]
    return next_question_ids

def subject_20(last_subject, second_last_subject):
    if last_subject[1] == '1' or second_last_subject[1] == '1':
        next_question_ids = [21, 22, 23]
    else:
        next_question_ids = [22, 23]
    return next_question_ids

def subject_23(last_subject, second_last_subject):
    if last_subject[1] == '1' or second_last_subject[1] == '1':
        next_question_ids = [24, 25, 26]
    else:
        next_question_ids = [25, 26]
    return next_question_ids

def subject_26(last_subject, second_last_subject):
    if last_subject[1] == '1' or second_last_subject[1] == '1':
        next_question_ids = [27, 28, 29]
    else:
        next_question_ids = [28, 29]
    return next_question_ids

def subject_29(last_subject, second_last_subject):
    if last_subject[1] == '1' or second_last_subject[1] == '1':
        next_question_ids = [30, 31, 32]
    else:
        next_question_ids = [31, 32]
    return next_question_ids

def subject_32(last_subject, second_last_subject):
    if last_subject[1] == '1' or second_last_subject[1] == '1':
        next_question_ids = [33, 34, 35]
    else:
        next_question_ids = [34, 35]
    return next_question_ids

def calculate_socre(right_answre_num, all_question_num):
    '''
    :param right_answre_num:  正确的题目数量
    :param all_question_num:  所有题目数量
    :return:
    '''
    score = right_answre_num/all_question_num
    if score < 0.5:
        stars = 1
    elif score >= 0.5 and score < 0.9:
        stars = 2
    else:
        stars = 3
    return {'score': score, 'stars': stars}


import pandas as pd
import numpy as np

Q1 = [['bill_depth_mm', 'body_mass_g', 'bill_length_mm'], 10]
Q2 = [['species', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'], 10]
Q3 = [['island', 'sex'], 10]
Q4 = [pd.read_pickle('Q4.pkl'), 10]
Q5 = [pd.read_pickle('Q5.pkl'), 10]
Q6 = ["Adelie", 10]
Q7 = ['Torgersen', 10]
Q8 = ['Adelie', 10]
Q9 = ["bill_length_mm", 10]
Q10 = [['body_mass_g', 'flipper_length_mm'], 10]
# Q11 = [pd.read_pickle('Q11.pkl'), 10]
# Q12 = [pd.read_pickle('Q12.pkl'), 5]
# Q13 = [pd.read_pickle('Q13.pkl'), 10]
# Q14 = [pd.read_pickle('Q14.pkl'), 5]

ans = [Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10,]
       # Q11, Q12, Q13, Q14]


def is_iterable(obj):
    # obj는 리스트 또는 시리즈 또는 인덱스
    if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, pd.Index) or isinstance(obj, pd.Series):
        try:
            iter(obj)
            return True
        except TypeError:
            return False
    else:
        return False
        
# def are_lists_equal(user_ans, ans):
#     if is_iterable(user_ans):
#         user_ans = list(user_ans)
#         return sorted(user_ans) == sorted(ans)
#     else:
#         return False

def are_value_equal(user_ans, ans):
    if user_ans.lower() == answer.lower():
        return True
    else:
        return False
        
def are_lists_equal(user_ans, ans):
    # 그냥 str을 원하는 정답인데 [str] 이렇게 답을 제출해서
    # 여기로 들어 올수 있음
    # 요소가 하나뿐인 리스트라면 다시 다른 함수로 보내기
    if len(user_ans) == 1:
        result = are_value_equal(user_ans[0], ans)
        return result
    else:
        if is_iterable(user_ans):
            user_ans = list(user_ans)
            return sorted([item.lower() if isinstance(item, str) else item for item in user_ans]) == \
            sorted([item.lower() if isinstance(item, str) else item for item in ans])
        else:
            return False


def are_df_equal(user_ans, ans):
    # 두 데이터프레임의 컬럼 순서를 동일하게 만들기
    # 컬럼이 아에 다를 수 있음, 컬럼 비교 부터 먼저 하기
    if list(user_ans.columns.sort_values()) != list(ans.columns.sort_values()):
        return False
        
    user_ans = user_ans[ans.columns]
    
    # 두 데이터프레임을 정렬하기 (여기서는 'A' 컬럼을 기준으로 정렬)
    user_ans = user_ans.sort_values(by=['bill_length_mm', 'bill_depth_mm']).reset_index(drop=True)
    ans = ans.sort_values(by=['bill_length_mm',	'bill_depth_mm']).reset_index(drop=True)
    
    # 두 데이터프레임 비교, 벨류 비교 둘중 하나만 맞으면 됨
    return user_ans.equals(ans) or np.all(user_ans.values == ans.values)

    
def are_series_equal(user_ans, ans):
    user_ans = user_ans.sort_index().reset_index(drop=True)
    ans = ans.sort_index().reset_index(drop=True)
    
    # 두 시리즈 비교
    return user_ans.equals(ans)
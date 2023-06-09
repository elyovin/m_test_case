import numpy as np
import pandas as pd

from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportions_ztest


def get_result_test_independence_1(
        df: pd.DataFrame, work_days: int,
        significance_level: float) -> tuple[pd.DataFrame, str]:
    men_more = len(df.query(
        f'`Пол` == "М" and `Количество больничных дней` > {work_days}'
    ))
    men_less = len(df.query(
        f'`Пол` == "М" and `Количество больничных дней` <= {work_days}'
    ))

    women_more = len(df.query(
        f'`Пол` == "Ж" and `Количество больничных дней` > {work_days}'
    ))
    women_less = len(df.query(
        f'`Пол` == "Ж" and `Количество больничных дней` <= {work_days}'
    )) 

    contingency_table = pd.DataFrame(
        [[men_less, men_more], [women_less, women_more]],
        columns=[f'Количество больничных дней <= {work_days}',
                 f'Количество больничных дней > {work_days}'],
        index=['М', 'Ж']
    )

    res = chi2_contingency(contingency_table)
    if res.pvalue < significance_level:
        result = 'Отколняем нулевую гипотезу'
    else:
        result = 'Не можем отклонить нулевую гипотезу'
    
    return contingency_table, result


def get_result_test_independence_2(
        df: pd.DataFrame, work_days: int, age: int,
        significance_level: float) -> tuple[pd.DataFrame, str]:
    young_more = len(df.query(
        f'`Возраст` < {age} and `Количество больничных дней` > {work_days}'
    ))
    young_less = len(df.query(
        f'`Возраст` < {age} and `Количество больничных дней` <= {work_days}'
    ))

    old_more = len(df.query(
        f'`Возраст` >= {age} and `Количество больничных дней` > {work_days}'
    ))
    old_less = len(df.query(
        f'`Возраст` >= {age} and `Количество больничных дней` <= {work_days}'
    )) 

    contingency_table = pd.DataFrame(
        [[young_less, young_more], [old_less, old_more]],
        columns=[f'Количество больничных дней <= {work_days}',
                 f'Количество больничных дней > {work_days}'],
        index=[f'Возраст < {age}', f'Возраст >= {age}']
    )

    res = chi2_contingency(contingency_table)
    if res.pvalue < significance_level:
        result = 'Отколняем нулевую гипотезу'
    else:
        result = 'Не можем отклонить нулевую гипотезу'

    return contingency_table, result

        
def get_result_stat_test_1(
        df: pd.DataFrame, work_days: int,
        significance_level: float) -> str:
    df_test_1 = df.query(f'`Количество больничных дней` > {work_days}')
    n_1, n_2 = df_test_1['Пол'].value_counts()[['М', 'Ж']]
    n_obs_1, n_obs_2 = df['Пол'].value_counts()[['М', 'Ж']]

    _, p_val = proportions_ztest([n_1, n_2], [n_obs_1, n_obs_2],
                                 alternative='larger')

    if p_val < significance_level:
        return 'Отколняем нулевую гипотезу'
    else:
        return 'Не можем отклонить нулевую гипотезу'


def get_result_stat_test_2(
        df: pd.DataFrame, work_days: int, age: int,
        significance_level: float) -> str:
    df_test_2 = df.query(f'`Количество больничных дней` > {work_days}')['Возраст']
    n_1, n_2 = np.sum(df_test_2 > age), np.sum(df_test_2 <= age)
    n_obs_1 = np.sum(df['Возраст'] > age)
    n_obs_2 = np.sum(df['Возраст'] <= age)

    _, p_val = proportions_ztest([n_1, n_2], [n_obs_1, n_obs_2],
                                 alternative='larger')
    if p_val < significance_level:
        return 'Отколняем нулевую гипотезу'
    else:
        return 'Не можем отклонить нулевую гипотезу'
import numpy as np
import pandas as pd

from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportions_ztest


CRITICAL_STAT_TEST_SAMPLE_SIZE = 30
CRITICAL_INDEP_TEST_SAMPLE_SIZE = 5


def get_result_test_independence_1(
        df: pd.DataFrame, work_days: int,
        significance_level: float) -> tuple[pd.DataFrame, bool, bool]:
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

    caution = (men_more < CRITICAL_INDEP_TEST_SAMPLE_SIZE
               or men_less < CRITICAL_INDEP_TEST_SAMPLE_SIZE
               or women_less < CRITICAL_INDEP_TEST_SAMPLE_SIZE
               or women_more < CRITICAL_INDEP_TEST_SAMPLE_SIZE)

    contingency_table = pd.DataFrame(
        [[men_less, men_more], [women_less, women_more]],
        columns=[f'Количество больничных дней <= {work_days}',
                 f'Количество больничных дней > {work_days}'],
        index=['М', 'Ж']
    )

    if caution:
        result = False
    else:
        res = chi2_contingency(contingency_table)
        result = res.pvalue < significance_level

    return contingency_table, result, caution


def get_result_test_independence_2(
        df: pd.DataFrame, work_days: int, age: int,
        significance_level: float) -> tuple[pd.DataFrame, bool, bool]:
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

    caution = (young_more < CRITICAL_INDEP_TEST_SAMPLE_SIZE
               or young_less < CRITICAL_INDEP_TEST_SAMPLE_SIZE
               or old_less < CRITICAL_INDEP_TEST_SAMPLE_SIZE
               or old_more < CRITICAL_INDEP_TEST_SAMPLE_SIZE)

    contingency_table = pd.DataFrame(
        [[young_less, young_more], [old_less, old_more]],
        columns=[f'Количество больничных дней <= {work_days}',
                 f'Количество больничных дней > {work_days}'],
        index=[f'Возраст < {age}', f'Возраст >= {age}']
    )

    if caution:
        result = False
    else:
        res = chi2_contingency(contingency_table)
        result = res.pvalue < significance_level

    return contingency_table, result, caution


def get_result_stat_test_1(
        df: pd.DataFrame, work_days: int,
        significance_level: float) -> tuple[bool, bool]:
    df_test_1 = df.query(f'`Количество больничных дней` > {work_days}')
    n_1, n_2 = df_test_1['Пол'].value_counts()[['М', 'Ж']]
    n_obs_1, n_obs_2 = df['Пол'].value_counts()[['М', 'Ж']]
    caution = (n_obs_1 < CRITICAL_STAT_TEST_SAMPLE_SIZE
               or n_obs_2 < CRITICAL_STAT_TEST_SAMPLE_SIZE)

    _, p_val = proportions_ztest([n_1, n_2], [n_obs_1, n_obs_2],
                                 alternative='larger')
    result = p_val < significance_level

    return result, caution


def get_result_stat_test_2(
        df: pd.DataFrame, work_days: int, age: int,
        significance_level: float) -> tuple[bool, bool]:
    df_test_2 = df.query(f'`Количество больничных дней` > {work_days}')['Возраст']
    n_1, n_2 = np.sum(df_test_2 > age), np.sum(df_test_2 <= age)
    n_obs_1 = np.sum(df['Возраст'] > age)
    n_obs_2 = np.sum(df['Возраст'] <= age)

    caution = (n_obs_1 < CRITICAL_STAT_TEST_SAMPLE_SIZE
               or n_obs_2 < CRITICAL_STAT_TEST_SAMPLE_SIZE)

    _, p_val = proportions_ztest([n_1, n_2], [n_obs_1, n_obs_2],
                                 alternative='larger')
    result = p_val < significance_level

    return result, caution

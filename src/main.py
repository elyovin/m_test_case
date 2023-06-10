import pandas as pd
import streamlit as st

from plot_generators import *
from test_generators import *


SHEET_ID = '1g0nPLuoD8KXYU5YeYJmj_NXbg8gcW2VTRgcaYUzGg0c'
WARNING_TEXT = 'Дальнейшее исследование невозможно'
REJECT_HYP_TEXT = 'Отклоняем нулевую гипотезу'
APPROVE_HYP_TEXT = 'Не можем отклонить нулевую гипотезу'
HYP_TEXT_RES = {True: REJECT_HYP_TEXT, False: APPROVE_HYP_TEXT}


def dispaly_hyp_1_plots(df: pd.DataFrame, work_days: int) -> None:
    fig_1 = get_hist_by_sex_work_days(df, work_days)
    fig_2 = get_whisker_plot_by_sex_work_days(df, work_days)
    st.write(fig_1)
    st.write(fig_2)


def display_hyp_2_plots(df: pd.DataFrame, work_days: int, age: int) -> None:
    fig_1 = get_hist_by_age_work_days(df, work_days, age)
    fig_2 = get_hist_by_age_work_days_small(df, work_days)
    st.write(fig_1)
    st.write(fig_2)


def display_test_indep_text() -> None:
    st.subheader('Проверка на независимость с помощью критерия хи-квадрат')
    st.markdown('$H_0$ : две группы независимы')
    st.markdown('$H_1$ : две группы не являются независимыми')


def display_result_test_indep(caution: bool, is_rejected: bool,
                              caution_msg: str,
                              significance_level: float) -> None:
    if caution:
        st.warning(caution_msg + ' ' + WARNING_TEXT)
    else:
        st.markdown(f'**{HYP_TEXT_RES[is_rejected]}** при уровне значимости'
                    + f' **{significance_level:.2f}**')

        if is_rejected:
            st.warning('Гипотеза о независимости не выполнена. '
                       + WARNING_TEXT)


def dispaly_result_stat_test(caution: bool, is_rejected: bool,
                             caution_msg: str,
                             significance_level) -> None:
    if caution:
        st.warning(caution_msg + ' ' + WARNING_TEXT)
    else:
        st.markdown(f'**{HYP_TEXT_RES[is_rejected]}** при уровне значимости'
                    + f' **{significance_level:.2f}**')


def display_stat_test_text_1(work_days: int) -> None:
    st.subheader('Проверка гипотезы с помощью двухпропорционного Z-теста')
    st.markdown('$p_1$ - пропорция **мужчин**, которые пропустили более '
                + f'{work_days} рабочих дней')
    st.markdown('$p_2$ - пропорция **женщин**, которые пропустили более '
                + f'{work_days} рабочих дней')
    st.markdown('$H_0: p_1 = p_2$')
    st.markdown('$H_1: p_1 > p_2$')


def display_stat_test_text_2(work_days: int, age: int) -> None:
    st.subheader('Проверка гипотезы с помощью двухпропорционного Z-теста')
    st.markdown(f'$p_1$ - пропорция работников, **старше {age} лет**,'
                + f' которые пропустили более {work_days} рабочих дней')
    st.markdown(f'$p_2$ - пропорция работников, **не старше {age} лет**,'
                + f' которые пропустили более {work_days} рабочих дней')
    st.markdown('$H_0: p_1 = p_2$')
    st.markdown('$H_1: p_1 > p_2$')


def display_hyp_1(df: pd.DataFrame) -> None:
    work_days = st.number_input(
        label='Количество пропущенных дней',
        min_value=df['Количество больничных дней'].min(),
        max_value=df['Количество больничных дней'].max() - 1,
        value=2,
        step=1,
        key='work_days'
    )

    st.header(f'Гипотеза: мужчины пропускают в течение года более {work_days}'
              + ' рабочих дней по болезни значимо чаще женщин.')
    dispaly_hyp_1_plots(df, work_days)
    display_test_indep_text()

    significance_level_indep = st.number_input(
        label='Уровень значимости',
        min_value=0.01,
        max_value=1.00,
        step=0.01,
        value=0.05,
        key='signifance_level_indep'
    )

    cont_table, is_rejected_indep, caution_indep = get_result_test_independence_1(
        df, work_days,
        significance_level_indep)

    st.write(cont_table)
    display_result_test_indep(caution_indep, is_rejected_indep,
                              'Слишком маленькая выборка.',
                              significance_level_indep)
    display_stat_test_text_1(work_days)
    significance_level_test = st.number_input(
        label='Уровень значимости',
        min_value=0.01,
        max_value=1.00,
        step=0.01,
        value=0.05,
        key='signifance_level_test'
    )

    is_rejected_stat, caution_stat = get_result_stat_test_1(
        df, work_days, significance_level_test)

    dispaly_result_stat_test(caution_stat, is_rejected_stat,
                             'Cлишком маленькая выборка. ',
                             significance_level_test)


def display_hyp_2(df: pd.DataFrame) -> None:
    work_days = st.number_input(
        label='Количество пропущенных дней',
        min_value=df['Количество больничных дней'].min(),
        max_value=df['Количество больничных дней'].max() - 1,
        value=2,
        step=1,
        key='work_days'
    )

    age = st.number_input(
        label='Возраст',
        min_value=df['Возраст'].min(),
        max_value=df['Возраст'].max() - 1,
        value=35,
        step=1,
        key='age'
    )

    st.header(f'Гипотеза: работники старше {age} лет пропускают в течение'
              + f' года более {work_days} рабочих дней по болезни значимо'
              + ' чаще своих более молодых коллег.')

    display_hyp_2_plots(df, work_days, age)
    display_test_indep_text()

    significance_level_indep = st.number_input(
        label='Уровень значимости',
        min_value=0.01,
        max_value=1.00,
        step=0.01,
        value=0.05,
        key='signifance_level_indep'
    )

    cont_table, is_rejected_indep, caution_indep = get_result_test_independence_2(
        df, work_days, age,
        significance_level_indep)

    st.write(cont_table)
    display_result_test_indep(caution_indep, is_rejected_indep,
                              'Слишком маленькая выборка.',
                              significance_level_indep)
    display_stat_test_text_2(work_days, age)

    significance_level_test = st.number_input(
        label='Уровень значимости',
        min_value=0.01,
        max_value=1.00,
        step=0.01,
        value=0.05,
        key='signifance_level_test'
    )

    is_rejected_stat, caution_stat = get_result_stat_test_2(
        df, work_days, age, significance_level_test)

    dispaly_result_stat_test(caution_stat, is_rejected_stat,
                             'Слишком маленькая выборка.',
                             significance_level_test)


def create_df(file) -> pd.DataFrame:
    if isinstance(file, str):
        file = f'https://docs.google.com/spreadsheets/d/{file}/gviz/tq?tqx=out:csv'

    df = pd.read_csv(file)
    new_columns = list(map(lambda x: x.strip('"'), df.columns[-1].split(',')))
    df[new_columns] = df[df.columns[0]].str.split(',', expand=True)
    df.drop(columns=df.columns[0], inplace=True)
    df['Пол'] = df['Пол'].str.strip('"')
    df['Количество больничных дней'] = df['Количество больничных дней'].astype(int)
    df['Возраст'] = df['Возраст'].astype(int)

    return df


def main() -> None:
    st.title('Cтатистика')

    is_uploaded = False
    sheets_id = st.text_input(
        label='Введите sheet id',
        help='sheet id is id of google spreadsheet',
        value=SHEET_ID
    )
    st.markdown('Или')
    uploaded_file = st.file_uploader('Выберите .csv файл',
                                     label_visibility='collapsed')

    if uploaded_file is not None or sheets_id is not None:
        try:
            df = create_df(uploaded_file or sheets_id)
            is_uploaded = True
        except Exception as exception:
            st.warning('Ошибка')
            st.info('Загрузите csv файл')
    else:
        st.info('Загрузите файл')

    if is_uploaded:
        st.subheader('Гипотеза')
        option = st.selectbox(
            'гипотеза',
            ('1', '2'),
            label_visibility='collapsed'
        )

        if option == '1':
            display_hyp_1(df)
        elif option == '2':
            display_hyp_2(df)


if __name__ == '__main__':
    main()

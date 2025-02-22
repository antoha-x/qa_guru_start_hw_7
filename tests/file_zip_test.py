QUANTITY_WORK_QA = 5
QA_PROFESSION = 'qa'
DEVOPS_PROFESSION = 'devops'
DEVOPS_CITY = 'Honolulu'
HR_CITY = 'Tbilisi'
HR_PROFESSION = 'hr'
HR_FIRST_NAME = 'Nicoli'
HR_LAST_NAME = 'Hartnett'


def test_working_qa(open_csv_file_in_archive):
    qa_list = [employee for employee in open_csv_file_in_archive if employee['profession'] == QA_PROFESSION]
    assert len(qa_list) == QUANTITY_WORK_QA, (f"Количество работающих тестировщиков {len(qa_list)}, "
                                              f"а должно быть {QUANTITY_WORK_QA}")


def test_working_devops_in_honolulu(open_pdf_file_in_archive):
    assert any([employee for employee in open_pdf_file_in_archive if
                employee['profession'] == DEVOPS_PROFESSION and employee['city'] == DEVOPS_CITY]), \
        f"В городе {DEVOPS_CITY} не найдено ни одного сотрудника с профессией {DEVOPS_PROFESSION}"


def test_working_hr(open_xlsx_file_in_archive):
    hr_city_list = [employee for employee in open_xlsx_file_in_archive if
                    employee['city'] == HR_CITY and employee['profession'] == HR_PROFESSION]
    assert any(hr for hr in hr_city_list if hr['firstname'] == HR_FIRST_NAME and hr['lastname'] == HR_LAST_NAME), \
        f"В городе {HR_CITY} не работает {HR_PROFESSION} c ФИО {HR_FIRST_NAME} {HR_LAST_NAME}"

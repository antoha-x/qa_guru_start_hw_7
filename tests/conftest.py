import csv
import os
import zipfile
from io import TextIOWrapper

import pytest
from openpyxl.reader.excel import load_workbook
from pypdf import PdfReader

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
TMP_DIR = os.path.join(PROJECT_DIR, "tmp")
RES_DIR = os.path.join(PROJECT_DIR, "resources")
ZIP_FILE_NAME = 'test.zip'
FILE_LIST_TO_ARCHIVE = ["employee.xlsx", "employee.pdf", "employee.csv"]


@pytest.fixture(scope="session")
def zip_files():
    if not os.path.exists(RES_DIR):
        os.mkdir(RES_DIR)

    with zipfile.ZipFile(os.path.join(RES_DIR, ZIP_FILE_NAME), "w") as zf:
        for file in FILE_LIST_TO_ARCHIVE:
            add_file = os.path.join(TMP_DIR, file)
            zf.write(add_file, os.path.basename(add_file))
    yield os.path.join(RES_DIR, ZIP_FILE_NAME)

    os.remove(os.path.join(RES_DIR, ZIP_FILE_NAME))
    os.rmdir(RES_DIR)


@pytest.fixture(scope="function")
def open_csv_file_in_archive(zip_files: str):
    with (zipfile.ZipFile(zip_files) as zip_file):
        with zip_file.open("employee.csv") as csv_file:
            file_data = csv.reader(TextIOWrapper(csv_file))
            headers = next(file_data)
            employees = [dict(zip(headers, i)) for i in file_data]

            yield employees


@pytest.fixture(scope="function")
def open_pdf_file_in_archive(zip_files: str):
    with (zipfile.ZipFile(zip_files) as zip_file):
        with zip_file.open("employee.pdf") as pdf_file:
            file_data = PdfReader(pdf_file)
            content = ''
            for page in file_data.pages:
                content = content + page.extract_text(extraction_mode="layout")
            content_lines = content.split('\n')
            headers = content_lines.pop(0).split()
            employees = [dict(zip(headers, i.split())) for i in content_lines]

            yield employees


@pytest.fixture(scope="function")
def open_xlsx_file_in_archive(zip_files: str):
    with (zipfile.ZipFile(zip_files) as zip_file):
        with zip_file.open("employee.xlsx") as xlsx_file:
            wb = load_workbook(xlsx_file)
            ws = wb.active
            content = list(ws.rows)
            headers = [cell.value for cell in content[0]]
            employees = [dict(zip(headers, [cell.value for cell in row])) for row in content]
            employees.pop(0)

            yield employees

import io

from openpyxl import Workbook


def create_excel(objects, exclude=None):
    """
    Функция создания excel
    objects принимает список объектов
    exclude принимает список лишних столбцов
    """
    workbook = Workbook()
    worksheet = workbook.active

    if objects:
        object = objects[0]
        field_names = []
        for column in object.__table__.columns:
            if exclude is None or column.key not in exclude:
                field_names.append(column.key)

        worksheet.append(field_names)

        for object in objects:
            row_data = []
            for field in field_names:
                row_data.append(getattr(object, field))
            worksheet.append(row_data)

    excel_data = io.BytesIO()
    workbook.save(excel_data)
    return excel_data


def create_excel_with_fields(objects, field_names, exclude=None):
    """
    Функция создания excel
    objects принимает список кортежей
    field_names принимает список названий столбцов
    exclude принимает список лишних столбцов
    """
    workbook = Workbook()
    worksheet = workbook.active

    if objects:
        if exclude:
            field_names = [
                field for field in field_names
                if field not in exclude
            ]

        worksheet.append(field_names)

        for object in objects:
            row_data = []
            for i, field in enumerate(field_names):
                row_data.append(object[i])
            worksheet.append(row_data)

    excel_data = io.BytesIO()
    workbook.save(excel_data)
    return excel_data

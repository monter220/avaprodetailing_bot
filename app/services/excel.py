import io

from openpyxl import Workbook


def create_excel(objects, exclude=None):
    '''
    Функция создания excel
    objects принимает список обектов
    exclude принимает список лишних столбцов
    '''
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
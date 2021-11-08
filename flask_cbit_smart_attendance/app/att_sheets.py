import openpyxl
import os
class Attendance(object):
    def __init__(self, roll_num1, roll_num2):
        self.roll_num1 = roll_num1
        self.roll_num2 = roll_num2
    
    def add_att(self):
        path = "C:/Users/prana/OneDrive/Desktop/web_dev/ocr_trial/flask_cbit_smart_attendance/"
        
        wb_obj = openpyxl.load_workbook(os.path.join(path, "xlwt att_sheets.xlsx"))
        
        sheet_obj = wb_obj.active

        sheet_obj.append([self.roll_num1, self.roll_num2])

        wb_obj.save('xlwt att_sheets.xlsx')



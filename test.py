
import os
import glob
import subprocess

def open_excel_files_in_current_dir():
    # カレントディレクトリ取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # .xlsx, .xls ファイルを取得
    excel_files = glob.glob(os.path.join(current_dir, '*.xlsx')) + glob.glob(os.path.join(current_dir, '*.xls'))
    if not excel_files:
        print('Excelファイルが見つかりません。')
        return
    for file in excel_files:
        print(f'{file} を開いています...')
        # WindowsでExcelファイルを開く
        os.startfile(file)
    print('完了しました！')

if __name__ == '__main__':
    open_excel_files_in_current_dir()

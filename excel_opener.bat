@echo off
REM このバッチファイルと同じディレクトリ内の全てのExcelファイル（.xlsx, .xls）とショートカットファイル（.lnk）を開く
for %%f in ("%~dp0*.xlsx" "%~dp0*.xls" "%~dp0*.lnk") do (
    echo %%fを開いています...
    start "" "%%f"
)
echo 完了しました！

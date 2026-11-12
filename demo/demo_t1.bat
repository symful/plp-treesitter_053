@call "%~dp0_env.bat"
echo on
cd tugas-1
python t1.py potongan1.py
python t1.py potongan1_rusak.py > %TEMP%\rusak.txt
findstr /C:"(ERROR" /C:"has_error: True" %TEMP%\rusak.txt

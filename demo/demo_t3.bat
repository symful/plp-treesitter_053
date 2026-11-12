@call "%~dp0_env.bat"
echo on
cd tugas-3
python rekap_fungsi.py contoh_q.py
python q.py contoh_q.py import.scm
python q.py contoh_q.py print.scm > %TEMP%\print.txt
find /c "@nama" %TEMP%\print.txt
python q.py contoh_panjang.py docstring.scm > %TEMP%\doc.txt
find /c "@doc" %TEMP%\doc.txt

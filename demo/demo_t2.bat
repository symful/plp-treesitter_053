@call "%~dp0_env.bat"
echo on
cd tugas-2
python jelajah.py kecil.py
python jelajah.py contoh_panjang.py > %TEMP%\a.txt
python jelajah_cursor.py contoh_panjang.py > %TEMP%\b.txt
fc %TEMP%\a.txt %TEMP%\b.txt
python jelajah.py contoh_panjang.py | find /c /v ""

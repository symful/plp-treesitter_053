@call "%~dp0_env.bat"
echo on
cd tugas-6
python cek.py uji
python cek.py C:\temp\requests > hasil_repo.txt
find /c "TODO" hasil_repo.txt
find /c "PANJANG" hasil_repo.txt
findstr /c:"utils.py:160" hasil_repo.txt

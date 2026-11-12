@call "%~dp0_env.bat"
echo on
cd tugas-1
python t1.py potongan1.py > output\t1_potongan1.txt
python t1.py potongan2.py > output\t1_potongan2.txt
python t1.py potongan3.py > output\t1_potongan3.txt
python t1.py potongan1_rusak.py > output\t1_potongan1_rusak.txt
python t1.py potongan2_rusak.py > output\t1_potongan2_rusak.txt
python t1.py potongan3_rusak.py > output\t1_potongan3_rusak.txt

cd ..\tugas-2
python jelajah.py kecil.py > output\t2_kecil.txt
python jelajah.py contoh_panjang.py > output\t2_panjang.txt

cd ..\tugas-3
python q.py contoh_q.py semua.scm > output\t3_semua.txt
python q.py contoh_q.py fungsi.scm > output\t3_fungsi.txt
python q.py contoh_q.py print.scm > output\t3_print.txt
python q.py contoh_q.py import.scm > output\t3_import.txt
python q.py contoh_panjang.py docstring.scm > output\t3_docstring_panjang.txt
python rekap_fungsi.py contoh_q.py > output\t3_rekap_fungsi.txt

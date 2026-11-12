@call "%~dp0_env.bat"
echo on
cd tugas-4\tree-sitter-filter
tree-sitter generate
tree-sitter test
python ..\filter_sql.py contoh.filter
python ..\filter_sql.py contoh2.filter

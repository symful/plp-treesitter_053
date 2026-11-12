@call "%~dp0_env.bat"
echo on
cd tugas-4\tree-sitter-filter
tree-sitter highlight contoh.filter
tree-sitter highlight contoh2.filter
tree-sitter parse contoh2.filter
fc queries\highlights.scm ..\..\tugas-5\highlights.scm

@echo off
chcp 65001 >nul

rem Folder proyek dihitung dari lokasi skrip ini, bukan dari path komputer pembuat.
cd /d "%~dp0.."
set "ROOT=%CD%"

if exist "%ROOT%\.venv-win\Scripts\activate.bat" (
    call "%ROOT%\.venv-win\Scripts\activate.bat"
) else (
    echo [peringatan] .venv-win tidak ditemukan. Jalankan: python -m venv .venv-win
)

rem CLI tree-sitter dan Node yang dibundel di folder tools.
set "PATH=%ROOT%\tools;%PATH%"

rem Compiler C dan Node dari instalasi umum; hanya ditambahkan jika benar-benar ada.
for %%D in (
    "C:\msys64\mingw64\bin"
    "%ProgramFiles%\nodejs"
    "C:\nvm4w\nodejs"
) do (
    if exist "%%~D" set "PATH=%%~D;%PATH%"
)

set "XDG_CONFIG_HOME=%ROOT%\.ts-config"
mode con: cols=150 lines=42 >nul

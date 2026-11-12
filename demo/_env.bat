chcp 65001 >nul
cd /d C:\Users\user\Project\tugasbatch\plp-treesitter
call .venv-win\Scripts\activate.bat
set PATH=%CD%\tools;C:\msys64\mingw64\bin;C:\nvm4w\nodejs;%PATH%
set XDG_CONFIG_HOME=%CD%\.ts-config
mode con: cols=150 lines=42 >nul

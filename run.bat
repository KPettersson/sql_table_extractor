@echo off
cd /d %~dp0
call .venv\Scripts\activate
python table_extractor.py
pause

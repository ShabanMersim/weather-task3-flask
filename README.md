# Task 3 — Weather (Flask)

Web приложение (Flask + Bootstrap), което:
- показва време за 5 случайни града,
- статистики (най-студен, средна температура),
- проверка по град.

## Стартиране (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

$env:OWM_API_KEY="YOUR_OPENWEATHER_KEY"
.\.venv\Scripts\python.exe .\app.py

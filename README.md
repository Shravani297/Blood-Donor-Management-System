# BloodCare — Blood Donor Management System

Desktop application built with **Python, Tkinter, and SQLite (SQL)**.

## Features
- Create account and login with hashed passwords
- First account in a fresh database becomes Admin; later accounts are regular Users
- Dashboard with donor/request statistics
- Register donors with input validation
- Search available donors by blood group and city/area
- Admin-only donor records and deletion
- Create and track emergency blood requests
- Admin can mark requests completed and manage user accounts
- Reports for blood group distribution and donor availability

## Requirements
- Python 3.10+ recommended
- Tkinter and SQLite are normally included with Python on Windows
- No third-party packages required

## Run in VS Code
1. Install Python from https://www.python.org/downloads/ (select **Add Python to PATH**).
2. Open this folder in VS Code.
3. Select **Terminal → New Terminal**.
4. Run `python main.py`.
5. Choose **Create New Account**. On a fresh database, the first account becomes Admin.

The app automatically creates `bloodcare.db`. Do not publish real donor personal information to GitHub.

## Push to GitHub
Create a new empty repository on GitHub, copy its HTTPS URL, then run these commands in the VS Code terminal from this folder. Replace the example URL with your repository URL:

```bash
git init
git add main.py README.md requirements.txt .gitignore
git commit -m "Add BloodCare donor management system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Your submission link will be `https://github.com/YOUR-USERNAME/YOUR-REPOSITORY`.
To submit just the code, open `main.py` in GitHub and copy that page's URL.

## Notes
- This is an academic desktop app; it does not automatically send SMS or contact donors.
- Use sample data for demonstrations and don't commit real phone numbers or personal/medical information.
- If an older `bloodcare.db` exists, its existing accounts remain. Back it up before deleting it to start fresh.

@echo off
title StockPro - Lancement en cours...
color 0B

echo ======================================================
echo           BIENVENUE SUR STOCKPRO V1.0
echo ======================================================
echo.
echo [1/3] Verification du serveur Python...

:: On verifie si Python est la, sinon on informe l'utilisateur
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe sur cette machine.
    pause
    exit
)

echo [2/3] Demarrage du moteur de base de donnees...
:: Lance le serveur en arriere-plan
start /min cmd /c "python manage.py runserver 0.0.0.0:8000"

echo [3/3] Ouverture de l'interface de gestion...
:: Attend 3 secondes que le serveur se lance bien
timeout /t 3 /nobreak >nul

:: Ouvre le navigateur par defaut sur la page admin
start http://127.0.0.1:8000/admin/

echo.
echo ======================================================
echo   LOGICIEL PRET ! NE FERMEZ PAS CETTE FENETRE
echo   PENDANT VOTRE TRAVAIL.
echo ======================================================
echo.
pause
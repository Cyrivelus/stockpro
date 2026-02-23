# --- CONFIGURATION DU SCRIPT ---
$ErrorActionPreference = "Stop"
$DossierProjet = "C:\xampp\htdocs\stockpro"

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "   INSTALLATION AUTOMATIQUE DE STOCKPRO V1.0" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

# 1. Verification des droits Administrateur
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "[!] Veuillez lancer ce script en tant qu'ADMINISTRATEUR (Clic droit > Executer avec PowerShell)." -ForegroundColor Red
    pause
    exit
}

# 2. Deplacement vers le dossier projet
if (Test-Path $DossierProjet) {
    Set-Location $DossierProjet
    Write-Host "[OK] Dossier projet trouve." -ForegroundColor Green
} else {
    Write-Host "[ERREUR] Le dossier $DossierProjet est introuvable." -ForegroundColor Red
    pause
    exit
}

# 3. Verification de Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "[OK] Python detecte." -ForegroundColor Green
} else {
    Write-Host "[!] Python n'est pas installe. Ouverture de la page de telechargement..." -ForegroundColor Red
    Start-Process "https://www.python.org/downloads/"
    pause
    exit
}

# 4. Installation des dependances (Requirements)
Write-Host "[...] Installation des bibliotheques (Patientez...)" -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 5. Preparation de la Base de Donnees
Write-Host "[...] Configuration de la base de donnees..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

# 6. Creation du compte Admin (Interactif)
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "   CREATION DU COMPTE ADMINISTRATEUR PRINCIPAL" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "Note: Le mot de passe ne s'affichera pas pendant la saisie." -ForegroundColor Gray
python manage.py createsuperuser

# 7. SECURISATION ET MASQUAGE DU CODE SOURCE
Write-Host "[...] Securisation des dossiers sources..." -ForegroundColor Yellow
# Masquer les dossiers de code
attrib +h +s "C:\xampp\htdocs\stockpro\apps"
attrib +h +s "C:\xampp\htdocs\stockpro\stockpro"
# Masquer les fichiers de configuration technique
attrib +h +s "C:\xampp\htdocs\stockpro\requirements.txt"
attrib +h +s "C:\xampp\htdocs\stockpro\.env" 2>$null # Masque le fichier de cle secrete s'il existe

Write-Host "======================================================" -ForegroundColor Green
Write-Host "   INSTALLATION TERMINEE AVEC SUCCES !" -ForegroundColor Green
Write-Host "   Le code source a ete securise et masque." -ForegroundColor Gray
Write-Host "   Lancez maintenant : DEMARRER_STOCKPRO.bat" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green

pause
@echo off
setlocal

echo ==========================================
echo   AI Pothole Detection - Project Setup
echo ==========================================
echo.

REM Go to the folder where this BAT file is located
cd /d "%~dp0"

echo Creating folders...
echo.

REM -----------------------------
REM Main folders
REM -----------------------------
if not exist "app" mkdir "app"

if not exist "src" mkdir "src"
if not exist "src\detection" mkdir "src\detection"
if not exist "src\preprocessing" mkdir "src\preprocessing"
if not exist "src\utils" mkdir "src\utils"

if not exist "api" mkdir "api"

if not exist "data" mkdir "data"
if not exist "data\train" mkdir "data\train"
if not exist "data\valid" mkdir "data\valid"
if not exist "data\test" mkdir "data\test"
if not exist "data\my_test" mkdir "data\my_test"

if not exist "models" mkdir "models"

if not exist "training" mkdir "training"

if not exist "tests" mkdir "tests"

if not exist "logger" mkdir "logger"

if not exist "mlruns" mkdir "mlruns"

if not exist "notebooks" mkdir "notebooks"

if not exist "scripts" mkdir "scripts"

if not exist "deployment" mkdir "deployment"


echo Creating files...
echo.

REM -----------------------------
REM App
REM -----------------------------
if not exist "app\app.py" type nul > "app\app.py"


REM -----------------------------
REM Detection
REM -----------------------------
if not exist "src\detection\detector.py" type nul > "src\detection\detector.py"

if not exist "src\detection\voice_alert.py" type nul > "src\detection\voice_alert.py"


REM -----------------------------
REM Preprocessing
REM -----------------------------
if not exist "src\preprocessing\image_processing.py" type nul > "src\preprocessing\image_processing.py"


REM -----------------------------
REM Utils
REM -----------------------------
if not exist "src\utils\config.py" type nul > "src\utils\config.py"


REM -----------------------------
REM FastAPI
REM -----------------------------
if not exist "api\main.py" type nul > "api\main.py"


REM -----------------------------
REM Dataset YAML files
REM -----------------------------
if not exist "data\data.yaml" type nul > "data\data.yaml"

if not exist "data\pothole_test.yaml" type nul > "data\pothole_test.yaml"


REM -----------------------------
REM Training
REM -----------------------------
if not exist "training\train.py" type nul > "training\train.py"

if not exist "training\evaluate_model.py" type nul > "training\evaluate_model.py"


REM -----------------------------
REM Tests
REM -----------------------------
if not exist "tests\test_detector.py" type nul > "tests\test_detector.py"

if not exist "tests\test_logger.py" type nul > "tests\test_logger.py"

if not exist "tests\test_api.py" type nul > "tests\test_api.py"


REM -----------------------------
REM Logger
REM -----------------------------
if not exist "logger\detection_logger.py" type nul > "logger\detection_logger.py"

if not exist "logger\detection_logs.csv" type nul > "logger\detection_logs.csv"


REM -----------------------------
REM Scripts
REM -----------------------------
if not exist "scripts\predict.py" type nul > "scripts\predict.py"


REM -----------------------------
REM Deployment
REM -----------------------------
if not exist "deployment\Dockerfile" type nul > "deployment\Dockerfile"

if not exist "deployment\docker-compose.yml" type nul > "deployment\docker-compose.yml"


REM -----------------------------
REM Root files
REM -----------------------------
if not exist ".gitignore" type nul > ".gitignore"

if not exist ".env.example" type nul > ".env.example"

if not exist "requirements.txt" type nul > "requirements.txt"

if not exist "README.md" type nul > "README.md"

if not exist "LICENSE" type nul > "LICENSE"


echo.
echo ==========================================
echo   Project structure created successfully!
echo ==========================================
echo.

tree /F

echo.
pause
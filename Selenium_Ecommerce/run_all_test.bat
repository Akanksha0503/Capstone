@echo off
title  Pytest Command Reference & Runner Guide
color 0A

echo ========================================================
echo           Selenium E-Commerce Pytest Runner
echo ========================================================
echo.
echo Project Folder: %CD%
echo Python Version:
python --version
echo.

REM =======================================================
REM  Basic Run
REM =======================================================
echo .  1. Running all tests normally...
pytest -v
echo

REM =======================================================
REM   Allure + HTML Report
REM =======================================================
echo .  2. Running tests with Allure + HTML report...
pytest -v --alluredir=reports/allure-results --html=reports/report.html --self-contained-html
echo " HTML report saved at: reports/report.html"
echo


REM =======================================================
REM  Sequential Execution (Run selected markers)
REM =======================================================
echo  . Sequential: Running tests by marker (login, search, add_customer)...
pytest tests/ -m "login or search or add_customer" -v --alluredir=reports/allure-results --html=reports/seq_report.html --self-contained-html
echo.
echo  Sequential HTML report saved at: reports\seq_report.html
echo.

REM =======================================================
REM  Parallel Execution (Auto-detect cores)
REM =======================================================
echo   2. Parallel: Running tests on all available CPU cores...
pytest tests/ -n auto -v --alluredir=reports/allure-parallel --html=reports/parallel_report.html --self-contained-html
echo.
echo  Parallel HTML report saved at: reports\parallel_report.html
echo.

REM =======================================================
REM Specific File Execution
REM =======================================================
echo   3. Running a specific test file: test_custadd.py ...
pytest tests\test_custadd.py -v -s --alluredir=reports/allure-specific --html=reports/specific_report.html --self-contained-html
echo.
echo Specific test HTML report saved at: reports\specific_report.html
echo.

REM =======================================================
REM  Headless Mode (for CI/CD - Manual Enable)
REM =======================================================
echo   4. Headless Execution (requires enabling --headless in setup fixture)
echo  To use headless mode, open your setup() fixture and UNCOMMENT:
echo     options.add_argument("--headless")
echo     options.add_argument("--disable-gpu")
echo.
echo   Skipping actual headless run (manual activation required).
echo.

REM =======================================================
REM Retry Failed Tests Automatically
REM =======================================================
echo   5. Retrying failed tests up to 2 times...
pytest --reruns 2 --reruns-delay 3 -v --alluredir=reports/allure-retry --html=reports/retry_report.html --self-contained-html
echo.
echo  Retry report saved at: reports\retry_report.html
echo.

REM =======================================================
REM  Stop on First Failure (Debug Mode)
REM =======================================================
echo   6. Debug mode — Stop on first failure...
pytest -x -v --alluredir=reports/allure-debug --html=reports/debug_report.html --self-contained-html
echo.
echo  Debug report saved at: reports\debug_report.html
echo.

REM =======================================================
REM  Collect Tests (Dry Run)
REM =======================================================
echo ⚙  7. Listing all discovered test cases (no execution)...
pytest --collect-only
echo.

REM =======================================================
REM  Full Regression (All Tests Sequential)
REM =======================================================
echo ️  8. Running full regression suite sequentially...
pytest tests/ -v --alluredir=reports/allure-full --html=reports/full_report.html --self-contained-html
echo.
echo  Full regression HTML report saved at: reports\full_report.html
echo.

echo ================================================
echo  Running Customer Search Test
echo ================================================

:: Run tests and generate both HTML + Allure result files
pytest Selenium_Ecommerce/tests/test_custsearch.py -v -s --alluredir=Selenium_Ecommerce/reports/allure-custsearch --html=Selenium_Ecommerce/reports/custsearch_report.html --self-contained-html

echo  Pytest execution complete.
echo ================================================
echo ⚙ Generating Allure HTML report...
echo ================================================

:: Generate permanent Allure HTML dashboard
allure generate Selenium_Ecommerce/reports/allure-custsearch -o Selenium_Ecommerce/reports/allure-report --clean

echo  Allure report generated successfully.
echo  Location: Selenium_Ecommerce\reports\allure-report\
start Selenium_Ecommerce\reports\allure-report\index.html

REM =======================================================
REM  Summary
REM =======================================================
echo ===============================================
echo   All Test Commands Executed Successfully
echo ===============================================
echo.
echo  Check reports folder for:
echo   • Allure raw results:  reports\allure-*
echo   • HTML reports:        reports\*_report.html
echo.
echo To view Allure report visually:
echo   allure serve reports\allure-results
echo ===============================================
pause

@echo off
REM Script per formattare le cartelle src, dist, src1 e src2

REM Definisci i percorsi delle cartelle
set SRC_DIR=src
set DIST_DIR=dist
set SRC1_DIR=src1
set SRC2_DIR=src2

REM Verifica se le cartelle esistono e le elimina
if exist "%SRC_DIR%" (
    echo Eliminando la cartella %SRC_DIR%...
    rmdir /s /q "%SRC_DIR%"
)

if exist "%DIST_DIR%" (
    echo Eliminando la cartella %DIST_DIR%...
    rmdir /s /q "%DIST_DIR%"
)

if exist "%SRC1_DIR%" (
    echo Eliminando la cartella %SRC1_DIR%...
    rmdir /s /q "%SRC1_DIR%"
)

if exist "%SRC2_DIR%" (
    echo Eliminando la cartella %SRC2_DIR%...
    rmdir /s /q "%SRC2_DIR%"
)

REM Ricrea le cartelle
echo Creando le cartelle %SRC_DIR%, %DIST_DIR%, %SRC1_DIR% e %SRC2_DIR%...
mkdir "%SRC_DIR%"
mkdir "%DIST_DIR%"
mkdir "%SRC1_DIR%"
mkdir "%SRC2_DIR%"

echo Formattazione completata.
pause
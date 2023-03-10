set targetdir=%~dp0target

IF NOT EXIST "%targetdir%" mkdir %targetdir%

javac -sourcepath %~dp0src -d %targetdir% -cp %~dp0lib/ECLA.jar;%~dp0lib/DTNConsoleConnection.jar; %~dp0src/core/*.java %~dp0src/movement/*.java %~dp0src/report/*.java %~dp0src/routing/*.java %~dp0src/gui/*.java %~dp0src/input/*.java %~dp0src/applications/*.java %~dp0src/interfaces/*.java %~dp0src/buffermanagement/*.java %~dp0src/sendingpolicy/*.java %~dp0src/droppolicy/*.java %~dp0src/attacks/*.java



IF NOT EXIST "%targetdir%\gui\buttonGraphics" (
	mkdir %targetdir%\gui\buttonGraphics
	copy %~dp0src\gui\buttonGraphics\* %targetdir%\gui\buttonGraphics\
)

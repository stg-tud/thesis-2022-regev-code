targetdir=target

if [ ! -d "$targetdir" ]; then mkdir $targetdir; fi

javac -encoding ISO-8859-1 -sourcepath src -d $targetdir -cp lib/ECLA.jar:lib/DTNConsoleConnection.jar src/core/*.java src/movement/*.java src/report/*.java src/routing/*.java src/gui/*.java src/input/*.java src/applications/*.java src/interfaces/*.java src/buffermanagement/*.java src/sendingpolicy/*.java src/droppolicy/*.java src/attacks/*.java
if [ ! -d "$targetdir/gui/buttonGraphics" ]; then cp -R src/gui/buttonGraphics target/gui/; fi
	

[Setup]
AppName=Android Tool
AppVersion=0.2.0
AppPublisher=Gissa333
DefaultDirName={autopf}\AndroidTool
DefaultGroupName=Android Tool
OutputDir=Output
OutputBaseFilename=AndroidTool-Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
DisableProgramGroupPage=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "..\dist\AndroidTool.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Android Tool"; Filename: "{app}\AndroidTool.exe"
Name: "{group}\إلغاء التثبيت"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Android Tool"; Filename: "{app}\AndroidTool.exe"

[Run]
Filename: "{app}\AndroidTool.exe"; Description: "تشغيل Android Tool"; Flags: postinstall nowait skipifsilent
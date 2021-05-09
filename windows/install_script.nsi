!define PRODUCT_NAME "TypusPocus"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_PUBLISHER "Facundo Batista"
!define PRODUCT_WEB_SITE "http://typuspocus.taniquetil.com.ar/"

!include "MUI2.nsh"
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "${PRODUCT_NAME}_Setup.exe"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"

!define MUI_ABORTWARNING
!define MUI_ICON "windows\typuspocus.ico"
!define MUI_HEADERIMAGE
!insertmacro MUI_PAGE_WELCOME
!define MUI_LICENSEPAGE
!insertmacro MUI_PAGE_LICENSE "gpl-2.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
LicenseData "gpl-2.txt"
DirText " "
ShowInstDetails show

Section "Main"
SetOutPath "$INSTDIR"
File /r "dist\__main__\"
CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\__main__.exe"
SectionEnd

!define MUI_FINISHPAGE_RUN "$INSTDIR\__main__.exe"
!define MUI_FINISHPAGE_LINK "Sitio web del proyecto"
!define MUI_FINISHPAGE_LINK_LOCATION "${PRODUCT_WEB_SITE}"

; these two goes in the end
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "Spanish"

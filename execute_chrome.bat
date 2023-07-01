if not exist "C:\chromeprofileDebug" mkdir "C:\chromeprofileDebug"
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dirs="C:\chromeprofileDebug"
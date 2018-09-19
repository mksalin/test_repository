// Signing: https://brightinventions.pl/blog/resigining-apk-manually/
//create keystore
"C:\Program Files (x86)\Java\jre1.8.0_181\bin\keytool.exe" -genkey -v -keystore C:\Users\markk\my-keystore.keystore -alias my-alias -keyalg RSA -keysize 2048 -validity 10000

// test keystore
"C:\Program Files (x86)\Java\jre1.8.0_181\bin\keytool.exe" -list -keystore C:\Users\markk\my-keystore.keystore -v -storepass android

// sign apk
C:\Users\markk\AppData\Local\Android\Sdk\build-tools\28.0.2\apksigner sign --ks C:\Users\markk\my-keystore.keystore --out C:\Users\markk\Documents\GitHub\test_repository\Ionic_test_app\myIonicTestApp\platforms\android\app\build\outputs\apk\release\my-app-release.apk C:\Users\markk\Documents\GitHub\test_repository\Ionic_test_app\myIonicTestApp\platforms\android\app\build\outputs\apk\release\app-release-unsigned.apk

// verify
C:\Users\markk\AppData\Local\Android\Sdk\build-tools\28.0.2\apksigner verify C:\Users\markk\Documents\GitHub\test_repository\Ionic_test_app\myIonicTestApp\platforms\android\app\build\outputs\apk\release\my-app-release.apk
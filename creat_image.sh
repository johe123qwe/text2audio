#!/bin/bash

# 安装 brew install create-dmg
# rm -rf build dist  && pyinstaller build.spec && bash creat_image.sh
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# brew install create-dmg
mkdir -p ./dist/dmg

rm -r ./dist/dmg/*
cp -r "dist/txt2au.app" dist/dmg 
test -f "dist/txt2au.dmg" && rm "dist/txt2au.dmg"
create-dmg \
  --volname "txt2au" \
  --volicon "./icon/app.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "txt2au.app" 175 120 \
  --hide-extension "txt2au.app" \
  --app-drop-link 425 120 \
  "dist/txt2au.dmg" \
  "dist/dmg/"
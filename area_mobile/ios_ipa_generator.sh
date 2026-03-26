#!/bin/bash

echo "Cleaning..."
rm -rf build/ios/iphoneos/Payload
rm -f client.ipa

echo "Building Flutter iOS..."
flutter build ios --release --no-codesign

echo "Packaging .ipa..."
cd build/ios/iphoneos
mkdir Payload
cp -r Runner.app Payload/
zip -r ../../../client.ipa Payload

echo "Cleaning up..."
rm -rf Payload

echo ".ipa package created"

#!/bin/bash
echo "🛠 init.sh script has started!"
set -e

echo "📱 Booting Android emulator..."

$ANDROID_SDK_ROOT/emulator/emulator \
  -avd test_avd \
  -no-audio \
  -no-boot-anim \
  -no-window \
  -no-snapshot \
  -gpu swiftshader_indirect \
  -accel off \
  -verbose \
  > /tmp/emulator.log 2>&1 &

echo "🕓 Waiting for emulator to finish booting..."
adb wait-for-device
adb shell 'while [[ -z $(getprop sys.boot_completed) ]]; do sleep 1; done;'
echo "✅ Emulator booted."

echo "🚀 Starting Appium server..."
exec appium --address 0.0.0.0 --port 4723 --log-level debug




# #!/bin/bash

# set -e

# echo "📱 Booting Android emulator..."
# $ANDROID_SDK_ROOT/emulator/emulator -avd test_avd -no-window -no-audio -no-boot-anim -accel off &

# echo "🕓 Waiting for emulator to boot..."
# adb wait-for-device
# sleep 30

# echo "🧪 Verifying emulator is running..."
# adb shell getprop sys.boot_completed | grep 1 || (echo "❌ Emulator not ready"; exit 1)

# echo "🚀 Starting Appium server..."
# which node
# node -v
# which appium
# appium --version
# appium --address 0.0.0.0 --port 4723


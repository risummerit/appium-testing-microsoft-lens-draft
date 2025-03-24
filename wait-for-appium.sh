#!/usr/bin/env bash
set -e

echo "⏳ Waiting for Appium on emulator:4723 to be ready..."

# Keep checking until Appium returns HTTP 200
until curl -s -f emulator:4723/wd/hub/status > /dev/null; do
  echo "❗ Still waiting for Appium..."
  sleep 2
done

echo "✅ Appium is ready! Running tests..."
pytest -v --tb=short

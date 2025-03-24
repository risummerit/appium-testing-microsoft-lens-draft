FROM --platform=linux/amd64 ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_SDK_ROOT/emulator:$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl unzip zip git adb \
    openjdk-17-jdk \
    libglu1-mesa \
    libc6-i386 lib32stdc++6 lib32z1 \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Install newer Node.js version
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs

# Install Appium
RUN npm install -g appium@1.22.0 --unsafe-perm

# Install Android SDK command-line tools
RUN mkdir -p $ANDROID_SDK_ROOT/cmdline-tools && \
    curl -o sdk-tools.zip https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip && \
    unzip sdk-tools.zip -d $ANDROID_SDK_ROOT/cmdline-tools && \
    mv $ANDROID_SDK_ROOT/cmdline-tools/cmdline-tools $ANDROID_SDK_ROOT/cmdline-tools/latest && \
    rm sdk-tools.zip

# Fix SDK parsing
RUN mkdir -p ~/.android && touch ~/.android/repositories.cfg

# Accept licenses early (doesn't hurt)
RUN yes | sdkmanager --sdk_root=$ANDROID_SDK_ROOT --licenses || true

# ✅ Install Android platform + emulator + image (split to reduce parse errors)
RUN yes | sdkmanager --sdk_root=$ANDROID_SDK_ROOT "platform-tools"
RUN yes | sdkmanager --sdk_root=$ANDROID_SDK_ROOT "platforms;android-30"
RUN yes | sdkmanager --sdk_root=$ANDROID_SDK_ROOT "emulator"
# Fow Windows:
RUN yes | sdkmanager --sdk_root=$ANDROID_SDK_ROOT "system-images;android-30;google_apis;x86_64"
# M1/M2 Mac:
# RUN yes | sdkmanager --sdk_root=$ANDROID_SDK_ROOT "system-images;android-30;google_apis;arm64-v8a"

# Install supervisor in the Dockerfile
RUN apt-get update && apt-get install -y supervisor

# Accept licenses again, just in case
RUN yes | sdkmanager --sdk_root=$ANDROID_SDK_ROOT --licenses

# Create AVD
# Fow Windows:
RUN echo "no" | avdmanager create avd -n test_avd -k "system-images;android-30;google_apis;x86_64" --device "Nexus 5"
# M1/M2 Mac:
# RUN echo "no" | avdmanager create avd -n test_avd -k "system-images;android-30;google_apis;arm64-v8a" --device "pixel"

# # Copy and make init.sh executable
# COPY init.sh /init.sh
# RUN chmod +x /init.sh
# ENTRYPOINT ["/init.sh"]

COPY supervisord.conf /etc/supervisord.conf
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

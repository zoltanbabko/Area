FROM ghcr.io/cirruslabs/flutter:3.19.0 AS build

WORKDIR /app

COPY pubspec.* ./
COPY . .

COPY client.ipa /tmp/client.ipa

RUN flutter create --platforms=android .

RUN flutter pub get

ENV GRADLE_OPTS="-Dorg.gradle.jvmargs=-Xmx2048m -Dorg.gradle.daemon=false"

RUN flutter build apk --release

CMD ["sh", "-c", "cp build/app/outputs/flutter-apk/app-release.apk /shared/client.apk && cp /tmp/client.ipa /shared/client.ipa && echo 'Mobile ready' && sleep infinity"]
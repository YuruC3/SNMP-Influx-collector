#!/bin/sh
set -e

# Default to 1600 if not provided
PUID="${PUID:-1600}"
PGID="${PGID:-1600}"
USER="${USER:-pythusr}"
GROUP="${USER:-pythusr}"
CHOWNPATH="/app/snmpython"

# Create group if missing
if ! getent group "$GROUP" >/dev/null 2>&1; then
    addgroup -g "$PGID" "$GROUP"
fi

# Create user if missing
if ! id -u "$USER" >/dev/null 2>&1; then
    adduser -D -u "$PUID" -G "$GROUP" "$USER"
fi

# Fix permissions (only do this on /app/API)
chown -R "$PUID:$PGID" "$CHOWNPATH"

# Drop privileges & run command
exec su-exec "$PUID:$PGID" "$@"

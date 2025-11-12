#!/bin/sh
xdg-open "$(cd "$(dirname "$0")" && pwd)/public/index.html" >/dev/null 2>&1 &

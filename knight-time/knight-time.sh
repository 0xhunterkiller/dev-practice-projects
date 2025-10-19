#!/bin/sh
echo -ne '\033c\033]0;Knight Time\a'
base_path="$(dirname "$(realpath "$0")")"
"$base_path/knight-time.x86_64" "$@"

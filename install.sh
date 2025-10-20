#!/usr/bin/env bash

set -euo pipefail

VERSION="2.0.0-beta.2"

WHITE="\033[1;37m"
YELLOW="\033[1;33m"
GRAY="\033[1;30m"
GREEN="\033[1;32m"
RED_BOLD="\033[1;31m"
RESET="\033[0m"

log_debug() {
	printf "%b%s%b\n" "$GRAY" "$1" "$RESET"
}

log_info() {
	printf "%s\n" "$1"
}

log_warn() {
	printf "%b! %s%b\n" "$YELLOW" "$1" "$RESET"
}

log_fatal() {
	printf "%b✖ %s%b\n" "$RED_BOLD" "$1" "$RESET" >&2
}

log_success() {
	printf "%b%s%b\n" "$YELLOW" "$1" "$RESET"
}

require_command() {
	if ! command -v "$1" >/dev/null 2>&1; then
		log_fatal "Required command '$1' is missing."
		exit 1
	fi
}

version_lt() {
	if [[ "$1" == "$2" ]]; then
		return 1
	fi
	local smallest
	smallest=$(printf '%s\n%s\n' "$1" "$2" | sort -V | head -n1)
	[[ "$smallest" == "$1" ]]
}

run_with_spinner() {
	local message="$1"
	shift
	local temp_stdout
	local temp_stderr
	temp_stdout=$(mktemp)
	temp_stderr=$(mktemp)
	printf "$WHITE%s -$RESET" "$message"
	("$@" >"$temp_stdout" 2>"$temp_stderr") &
	local pid=$!
	local frames='-\|/'
	local i=0
	while kill -0 "$pid" >/dev/null 2>&1; do
		local idx=$((i % 4))
		local frame=${frames:idx:1}
		printf "\r$WHITE%s %c$RESET" "$message" "$frame"
		sleep 0.1
		i=$((i + 1))
	done
	if wait "$pid"; then
		printf "\r$GRAY%s [done]$RESET\n" "$message"
		rm -f "$temp_stdout" "$temp_stderr"
	else
		printf "\r$RED_BOLD%s [fail]$RESET\n" "$message"
		cat "$temp_stdout"
		cat "$temp_stderr" >&2
		rm -f "$temp_stdout" "$temp_stderr"
		exit 1
	fi
}

download_mango() {
	local dest="$1"
	local url
	for url in "${MANGO_SOURCE_URLS[@]}"; do
		if curl -sSfL "$url" -o "$dest"; then
			MANGO_FETCHED_FROM="$url"
			return 0
		fi
	done
	return 1

}
log_debug "Preparing Mango installer for version $VERSION"

for cmd in curl git mktemp install sort; do
	require_command "$cmd"
done

if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
	if command -v sudo >/dev/null 2>&1; then
		SUDO="sudo"
	else
		log_fatal "Root privileges are required. Please run as root or install sudo."
		exit 1
	fi
else
	SUDO=""
fi

MANGO_HOME="${HOME}/.mango"
MANGO_SUBMODULES_DIR="${MANGO_HOME}/.submodules"
MANGO_BUILTINS_DIR="${MANGO_SUBMODULES_DIR}/builtins"
MANGO_TEMPLATES_REGISTRY="${MANGO_HOME}/.templates.registry"
MANGO_SUBMODULES_REGISTRY="${MANGO_HOME}/.submodules.registry"
MANGO_BUILTINS_REPO="https://github.com/RayZh-hs/builtins.mango.git"
DEST_BIN="/usr/bin/mango"

MANGO_REF="${MANGO_INSTALL_REF:-${VERSION}}"
MANGO_FALLBACK_REF="${MANGO_FALLBACK_REF:-main}"
MANGO_SOURCE_URLS=(
	"https://raw.githubusercontent.com/RayZh-hs/Mango/${MANGO_REF}/src/mango"
	"https://raw.githubusercontent.com/RayZh-hs/Mango/${MANGO_FALLBACK_REF}/src/mango"
)
MANGO_FETCHED_FROM=""

if command -v mango >/dev/null 2>&1; then
	EXISTING_MANGO_PATH=$(command -v mango)
	INSTALLED_VERSION="$(mango --version 2>/dev/null | awk '{print $2}')"
	if [[ -z "${INSTALLED_VERSION}" ]]; then
		log_debug "Existing mango detected at ${EXISTING_MANGO_PATH}, version unknown. Removing it."
		$SUDO rm -f "$EXISTING_MANGO_PATH"
	elif version_lt "$INSTALLED_VERSION" "$VERSION"; then
		$SUDO rm -f "$EXISTING_MANGO_PATH"
		printf "%bUpdating mango $GREEN(${INSTALLED_VERSION} -> ${VERSION})$RESET.\n" "$GRAY"
	else
		log_info "Mango ${INSTALLED_VERSION} is already up to date."
		exit 0
	fi
fi

if [[ -d "$MANGO_HOME" && ! -d "${MANGO_HOME}/.submodules" ]]; then
	log_info "From Mango 2.0.0-alpha onward, home repos use submodules."
	log_info "Existing ~/.mango does not have submodules."
	log_warn "Remove ~/.mango and reinitialize? [y/N]"
	if ! read -r -p "> " RESPONSE; then
		log_fatal "No response received. Installation aborted."
		exit 1
	fi
	case "$RESPONSE" in
		[yY]|[yY][eE][sS])
			rm -rf "$MANGO_HOME"
			;;
		*)
			log_info "Keeping current ~/.mango. Installation stopped."
			exit 0
			;;
	esac
fi

mkdir -p "$MANGO_SUBMODULES_DIR"
mkdir -p "$MANGO_TEMPLATES_REGISTRY" "$MANGO_SUBMODULES_REGISTRY"

if [[ -d "$MANGO_BUILTINS_DIR" ]]; then
	rm -rf "$MANGO_BUILTINS_DIR"
fi

run_with_spinner "Cloning builtins library" git clone --depth 1 --quiet "$MANGO_BUILTINS_REPO" "$MANGO_BUILTINS_DIR"

printf '[builtins] *\n' >"${MANGO_HOME}/.instructions"

log_debug "Registered builtins in ${MANGO_HOME}/.instructions"

TEMP_BINARY=$(mktemp)
trap 'rm -f "$TEMP_BINARY"' EXIT

run_with_spinner "Downloading mango executable" download_mango "$TEMP_BINARY"

$SUDO install -m 0755 "$TEMP_BINARY" "$DEST_BIN"

log_success "Mango ${VERSION} installed to $DEST_BIN"
if [[ -n "$MANGO_FETCHED_FROM" ]]; then
	log_debug "Executable sourced from $MANGO_FETCHED_FROM"
fi
log_debug "> Run 'mango --version' to verify the installation."

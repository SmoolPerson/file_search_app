#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Install Homebrew if missing
if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install uv if missing
if ! command -v uv &>/dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install Java (Neo4j requires a JVM)
if ! command -v java &>/dev/null; then
    echo "Installing Java..."
    brew install openjdk
    # Make java available on PATH for this session
    export PATH="$(brew --prefix openjdk)/bin:$PATH"
fi

# Install Neo4j
if ! command -v neo4j &>/dev/null; then
    echo "Installing Neo4j..."
    brew install neo4j
fi

echo ""
echo "Dependencies installed. Run ./setup_neo4j.sh to configure the database."

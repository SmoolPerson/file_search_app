#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

NEO4J_USER="neo4j"
NEO4J_PASSWORD="password"
NEO4J_DATABASE="neo4j"

# Stop Neo4j so we can safely reset auth
echo "Stopping Neo4j..."
brew services stop neo4j 2>/dev/null || true
sleep 3

# Wipe the auth store so set-initial-password takes effect
NEO4J_AUTH_FILE="$(brew --prefix)/var/neo4j/data/dbms/auth"
if [ -f "$NEO4J_AUTH_FILE" ]; then
    rm -f "$NEO4J_AUTH_FILE"
    echo "Auth store cleared."
fi

# Set the password before starting
neo4j-admin dbms set-initial-password "$NEO4J_PASSWORD"
echo "Password set to '$NEO4J_PASSWORD'."

# Start Neo4j
echo "Starting Neo4j..."
brew services start neo4j

# Wait for Neo4j HTTP interface to be ready
echo "Waiting for Neo4j to be ready..."
until curl -s http://localhost:7474 > /dev/null 2>&1; do
    sleep 2
done
echo "Neo4j is up."



echo ""
echo "Neo4j setup complete. Add these to your environment before running start.sh:"
echo ""
echo "  export NEO4J_URI=bolt://localhost:7687"
echo "  export NEO4J_USERNAME=$NEO4J_USER"
echo "  export NEO4J_PASSWORD=$NEO4J_PASSWORD"
echo "  export NEO4J_DATABASE=$NEO4J_DATABASE"

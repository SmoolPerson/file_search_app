#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

NEO4J_USER="neo4j"
NEO4J_INITIAL_PASSWORD="neo4j"
NEO4J_PASSWORD="password"
NEO4J_DATABASE="filedb"

# Start Neo4j if not already running
if ! brew services list | grep -q "neo4j.*started"; then
    echo "Starting Neo4j..."
    brew services start neo4j
fi

# Wait for Neo4j HTTP interface to be ready
echo "Waiting for Neo4j to be ready..."
until curl -s http://localhost:7474 > /dev/null 2>&1; do
    sleep 2
done
echo "Neo4j is up."

# Change default password (only needed on first run — safe to ignore if already changed)
echo "Setting password..."
cypher-shell -u "$NEO4J_USER" -p "$NEO4J_INITIAL_PASSWORD" \
    "ALTER CURRENT USER SET PASSWORD FROM '$NEO4J_INITIAL_PASSWORD' TO '$NEO4J_PASSWORD';" \
    2>/dev/null && echo "Password set." || echo "Password already changed, skipping."

# Create the filedb database (requires Neo4j 5+ — skipped silently on Community if unsupported)
echo "Creating '$NEO4J_DATABASE' database..."
cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
    -d system \
    "CREATE DATABASE $NEO4J_DATABASE IF NOT EXISTS;" \
    2>/dev/null && echo "Database '$NEO4J_DATABASE' ready." \
    || echo "Could not create '$NEO4J_DATABASE' (Community Edition may not support multiple databases). Using default 'neo4j' database instead."

echo ""
echo "Neo4j setup complete. Add these to your environment before running start.sh:"
echo ""
echo "  export NEO4J_URI=bolt://localhost:7687"
echo "  export NEO4J_USERNAME=$NEO4J_USER"
echo "  export NEO4J_PASSWORD=$NEO4J_PASSWORD"
echo "  export NEO4J_DATABASE=$NEO4J_DATABASE"

#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

NEO4J_USER="neo4j"
NEO4J_PASSWORD="password"
NEO4J_DATABASE="filedb"

# Set initial password before first start (avoids interactive prompt)
# This is a no-op if Neo4j has already been started before
neo4j-admin dbms set-initial-password "$NEO4J_PASSWORD" 2>/dev/null || true

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

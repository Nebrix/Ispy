#!/bin/bash

DB_FILE="user_db.db"

if [ -e "$DB_FILE" ]; then
  echo "Database file '$DB_FILE' already exists. Exiting..."
  exit 1
fi

sqlite3 "$DB_FILE" <<EOF
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
EOF

if [ $? -eq 0 ]; then
  echo "Database and 'users' table created successfully in '$DB_FILE'."
else
  echo "Failed to create the database or 'users' table."
fi
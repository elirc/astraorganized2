package storage

import (
    "database/sql"
    "sync"
)

type DuckDBStore struct {
    db *sql.DB
    mu sync.RWMutex
}

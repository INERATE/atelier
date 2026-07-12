-- Atelier store (atelier.db) — schema v1. WAL mode set at connection time.
-- All agent access goes through the store MCP; responses serialized as TOON.

CREATE TABLE IF NOT EXISTS meta            (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS capabilities    (name TEXT PRIMARY KEY, available INTEGER,
                                            detail TEXT, checked_at TEXT);
CREATE TABLE IF NOT EXISTS projects        (id INTEGER PRIMARY KEY, name TEXT, stack TEXT,
                                            layout TEXT, auth_mode TEXT, hosting TEXT,
                                            project_md_path TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS plans           (id INTEGER PRIMARY KEY, project_id INT, title TEXT,
                                            body_md TEXT, status TEXT, model TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS done_criteria   (id INTEGER PRIMARY KEY, plan_id INT, criterion TEXT,
                                            check_kind TEXT,  -- manual|test|lint|perf|a11y|design
                                            passed INTEGER DEFAULT 0, evidence TEXT);
CREATE TABLE IF NOT EXISTS clarifications  (id INTEGER PRIMARY KEY, plan_id INT, question TEXT,
                                            answer TEXT, asked_at TEXT);
CREATE TABLE IF NOT EXISTS rules           (id INTEGER PRIMARY KEY, domain TEXT,  -- design|code|structure|auth|stack
                                            key TEXT, value TEXT,
                                            source TEXT,      -- core|overlay:<file>
                                            active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS design_guide_versions (id INTEGER PRIMARY KEY, path TEXT,
                                            kind TEXT,        -- core|overlay
                                            added_at TEXT, promoted INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS registry        (id INTEGER PRIMARY KEY, kind TEXT,  -- component|mcp|skill|tool|site
                                            name TEXT, source TEXT, install TEXT, usage TEXT,
                                            meta TEXT);
CREATE TABLE IF NOT EXISTS learning_events (id INTEGER PRIMARY KEY, kind TEXT,  -- image|video|url|code|skill|mcp
                                            path_or_url TEXT, summary TEXT, overlay_path TEXT,
                                            created_at TEXT);
CREATE TABLE IF NOT EXISTS asset_manifest  (id INTEGER PRIMARY KEY, src TEXT, out TEXT,
                                            kind TEXT, bytes_before INT, bytes_after INT);
CREATE TABLE IF NOT EXISTS activity_log    (id INTEGER PRIMARY KEY, actor TEXT, action TEXT,
                                            detail TEXT, at TEXT);
CREATE TABLE IF NOT EXISTS framework_map   (id INTEGER PRIMARY KEY, path TEXT, kind TEXT,  -- skill|agent|command|tool|template|doc
                                            purpose TEXT, load_when TEXT, links TEXT);

CREATE INDEX IF NOT EXISTS idx_rules_domain ON rules(domain, active);
CREATE INDEX IF NOT EXISTS idx_criteria_plan ON done_criteria(plan_id, passed);
CREATE INDEX IF NOT EXISTS idx_registry_kind ON registry(kind);

INSERT OR IGNORE INTO meta VALUES ('schema_version', '1');

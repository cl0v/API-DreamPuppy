#!/bin/bash

# cp gallery.db copy.db
sqlite3 copy.db < scripts/config.sql
sqlite3 copy.db < scripts/example.sql

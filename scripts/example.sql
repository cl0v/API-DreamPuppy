-- # Exec by running sqlite3 gallery.db < scripts/example.sql

-- SELECT * FROM users WHERE email IS '2';
-- SELECT LENGTH(hashed_password) FROM users WHERE id IS 2;
-- SELECT hashed_password FROM users WHERE id IS 2;
-- SELECT REPLACE(hashed_password, 'notreallyhashed', 'secureASFUCK') FROM users WHERE id IS 2;
-- SELECT typeof(is_active) FROM users WHERE id IS 4;
-- INSERT INTO users (email, hashed_password, is_active)  VALUES ('folgado@dalapa.com', 'semsenha', TRUE);
-- SELECT COUNT(*) from users;

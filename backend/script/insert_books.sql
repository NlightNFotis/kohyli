-- scripts/insert_books.sql
-- Inserts sample authors and sample books into the database.
-- This script uses SQLite-compatible "INSERT OR IGNORE" so it can be run multiple times safely.
-- Run against the SQLite DB file used by your app, for example:
--   sqlite3 kohyli.db < scripts/insert_books.sql
--
-- Note: Adjust IDs if they conflict with existing data in your DB.

-- Ensure authors exist (idempotent). Existing example authors are kept and new ones for the mock data are added.
INSERT OR IGNORE INTO author (id, first_name, last_name, biography) VALUES
  (1, 'J.R.R.', 'Tolkien', 'Fantasy author'),
  (2, 'George', 'Orwell', 'Dystopian author'),
  (10, 'Matt', 'Haig', 'Author of The Midnight Library'),
  (11, 'James', 'Clear', 'Author of Atomic Habits'),
  (12, 'Andy', 'Weir', 'Author of Project Hail Mary'),
  (13, 'Kristin', 'Hannah', 'Author of The Four Winds'),
  (14, 'Kazuo', 'Ishiguro', 'Author of Klara and the Sun'),
  (15, 'Michelle', 'Zauner', 'Author of Crying in H Mart'),
  (16, 'Frank', 'Herbert', 'Author of Dune'),
  (17, 'Tara', 'Westover', 'Author of Educated');

-- Insert 8 books modeled after the provided mockBooks array.
-- Several entries use published_date values within the last month to serve as "new arrivals".
INSERT OR IGNORE INTO book (id, title, author_id, isbn, price, published_date, description, stock_quantity, cover_image_url) VALUES
  (2001, 'The Midnight Library', 10, '978-1-250-00001-1', 15.99, '2025-08-20 10:00:00', 'A novel by Matt Haig about alternate lives.', 20, 'https://placehold.co/300x450/0ea5e9/ffffff?text=The+Midnight+Library'),
  (2002, 'Atomic Habits', 11, '978-1-250-00002-2', 19.99, '2025-07-15 09:00:00', 'Practical strategies for habit change by James Clear.', 30, 'https://placehold.co/300x450/38bdf8/ffffff?text=Atomic+Habits'),
  (2003, 'Project Hail Mary', 12, '978-1-250-00003-3', 18.50, '2025-08-05 12:00:00', 'A lone astronaut must save the earth in this sci-fi thriller.', 15, 'https://placehold.co/300x450/0ea5e9/ffffff?text=Project+Hail+Mary'),
  (2004, 'The Four Winds', 13, '978-1-250-00004-4', 22.00, '2024-11-01 00:00:00', 'Historical fiction by Kristin Hannah.', 12, 'https://placehold.co/300x450/38bdf8/ffffff?text=The+Four+Winds'),
  (2005, 'Klara and the Sun', 14, '978-1-250-00005-5', 16.75, '2025-08-10 08:30:00', 'A novel by Kazuo Ishiguro about an Artificial Friend.', 18, 'https://placehold.co/300x450/0ea5e9/ffffff?text=Klara+and+the+Sun'),
  (2006, 'Crying in H Mart', 15, '978-1-250-00006-6', 14.99, '2025-06-01 00:00:00', 'A memoir by Michelle Zauner.', 22, 'https://placehold.co/300x450/38bdf8/ffffff?text=Crying+in+H+Mart'),
  (2007, 'Dune', 16, '978-1-250-00007-7', 12.99, '1965-08-01 00:00:00', 'Classic science fiction by Frank Herbert.', 8, 'https://placehold.co/300x450/0ea5e9/ffffff?text=Dune'),
  (2008, 'Educated', 17, '978-1-250-00008-8', 17.00, '2018-02-18 00:00:00', 'A memoir by Tara Westover.', 14, 'https://placehold.co/300x450/38bdf8/ffffff?text=Educated');

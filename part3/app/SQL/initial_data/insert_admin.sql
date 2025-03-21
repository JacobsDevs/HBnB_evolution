-- Inserting into users table
INSERT INTO users (
  id,
  email,
  first_name,
  last_name,
  password,
  is_admin)
VALUES (
  '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
  'admin@hbnb.io',
  'Admin',
  'HBnB',
  '$2y$10$Xrilmf7skgLetD65nhVAzei./WSWfOM4AB9.AeBKm.Wiqg3goOy7.',
  1);

-- Inserting into amenities table
  INSERT INTO amenities (id, name) VALUES
  ('bbb533ac-e2b4-4599-b5fd-5eaa0ff085e5', 'WiFi'),
  ('8a3e5f01-4ef5-4fe6-8815-9ac58f9ae0d7', 'Swimming Pool'),
  ('47fabf38-8594-4220-979b-88f5a365f809', 'Air Conditioning');
  

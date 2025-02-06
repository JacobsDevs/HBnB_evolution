# Okky's `HBnB - UML` Playgound

## *==> The things to do <==*

**User Management:** `user_can` 
- Register
- Update details
- ID Level (host vs guest)

**Place Management:** `user_can_property`
- List their property with details (`attributes`)
    - Name
    - Description
    - Price
    - Location
    - List of amenities
        - Bedroom
        - Toilet
        - etc

**Review Management:** `user_can_review`
- leave review on property
- Rating system (`int / float`)
    - include comment

**Amenity Management** `user_can_clean`
- Manage amenities associated with property
    - *i visualize this as a clean service?* 
---

# *==> Rules: <==*

### *`user_entity`*

- (`first_name`)
- (`last_name`)
- (`email`)
- (`password`)
- (`admin`) == boolean (attribute required)
    - able to register (create)
    - edit user_entity
    - delete user_entity

### *`place_entity`*

- (`title`)
- (`description`)
- (`price`)
- (`latitude`)
- (`longitude`)
- (`owner`)
    - *link this via ID?*
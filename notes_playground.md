# Okky's `HBnB - UML` Playgound

## *==> The things users can do <==*

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
**--> Each `object` should be uniquely idetified by a `ID` <--** \
**--> `Creation` and `update` *<ins>datetime<ins>* should be registerd for all `entities` <--**



### 1. *`user_entity`*

- (`first_name`)
- (`last_name`)
- (`email`)
- (`password`)
- (`admin`) == boolean (attribute required)
    - able to register (create)
    - edit user_entity
    - delete user_entity

### 2. *`place_entity`*

- (`title`)
- (`description`)
- (`price`)
- (`latitude`)
- (`longitude`)
- (`owner`)
    - *link this via ID?*
- (`amenities`)
    - bathroom
    - cinema
    - toilet
    - sauna
    - pool
    - etc
- (`edit`)
    - ~~create~~
    - ~~update~~
    - ~~delete~~
    - ~~list (post/advertise)~~

### 3. *`review_entity`*
- (`review_place`)
    - `user` able to leave review on listing / property
    - ~~create~~
    - ~~update~~
    - ~~delete~~
    - ~~list by place~~
        - sort function?
- (`rating`)
- (`comment`)

### 4. *`amenity_entity`*
- (`name`)
- (`description`)
- ~~create~~
- ~~updated~~
- ~~deleted~~
- ~~listed~~

### 5. *`Global / Classes`*
- `create`
- `udpate`
- `delete`
- `list`

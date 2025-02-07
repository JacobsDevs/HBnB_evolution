# Okky's `HBnB - UML` Playgound

# *==> Rules: <==*
**--> Each `object` should be uniquely idetified by a `ID` <--** \
**--> `Creation` and `update` *<ins>datetime<ins>* should be registerd for all `entities` <--**



### 1. *`user_entity`*

- [x] (`first_name`)
- [x] (`last_name`)
- [x] (`email`)
- [x] (`password`)
- [x] (`admin`) == boolean (attribute required)
    - able to register (create)
    - edit user_entity
    - delete user_entity

### 2. *`place_entity`*

- [ ] (`title`)
- [ ] (`description`)
- [ ] (`price`)
- [ ] (`latitude`)
- [ ] (`longitude`)
- [ ] (`owner`)
    - *link this via ID?*
- [ ] (`amenities`)
    - bathroom
    - cinema
    - toilet
    - sauna
    - pool
    - etc
- [ ] (`edit`)
    - ~~create~~
    - ~~update~~
    - ~~delete~~
    - ~~list (post/advertise)~~

### 3. *`review_entity`*
- [x] (`review_place`)
    - [x] `user` able to leave review on listing / property
    - ~~create~~
    - ~~update~~
    - ~~delete~~
    - ~~list by place~~
        - sort function?
- [x] (`rating`)
- [x] (`comment` / `description`)

### 4. *`amenity_entity`*
- [x] (`name`)
- [x] (`description`)
- ~~create~~
- ~~updated~~
- ~~deleted~~
- ~~listed~~

### 5. *`Global / Classes`*
- [ ] `create`
- [ ] `udpate`
- [ ] `delete`
- [ ] `list`

---
---


## ==> HL_PCK_Diagram.io <== 
- Presentation Layer
    - Handles user interaction (desktop/mobile)
    - Display properties listings (gallery)
    - Booking Management

- Facade Pattern
    - Simplify communication to each layer
    - reduce complexity 
    - promote encapsulation (OOP)

- Business Logic Layer
    - Core Application logic
    - User Management
    - Property listing operations/management
    - booking transactions
    - Review management

- Persistence Layer
    - Database Repositories (SQL)
    - Database management
        - users
        - listings


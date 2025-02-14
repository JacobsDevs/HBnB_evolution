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

- [x] (`title`)
- [x] (`description`)
- [x] (`price`)
- [ ] (`latitude`)
- [ ] (`longitude`)
- [x] (`owner`)
    - *link this via ID?*
- [x] (`amenities`)
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
    - Booking Management
    - Handles user interaction (desktop/mobile)
    - Display properties listings (gallery)

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

## ==> Class Diagram <==
```mermaid
classDiagram
direction TB
	namespace PresentationLayer {
        class UserServices {
	        +register()
	        +login()
	        +updateProfile()
	        +deleteAccount()
	        +convertToOwner()
	        +getGuestHistory()
        }
        class PlaceServices {
	        +getPublicDetails()
	        +getFullDetails()
	        +createPlace()
	        +updatePlace()
	        +deletePlace()
	        +searchByAmenities()
	        +checkAvailability()
        }
        class ReviewServices {
	        +createPlaceReview()
	        +createGuestReview()
	        +updateReview()
	        +getPublicRating()
	        +getFullReviews()
	        +checkStayCompletion()
        }
        class AmenityServices {
	        +listAmenities()
	        +addAmenity()
	        +updateAmenity()
	        +deleteAmenity()
	        +searchPlacesByAmenity()
	        +getSuggestedAmenities()
        }
        class BookingServices {
	        +createBooking()
	        +updateBooking()
	        +cancelBooking()
	        +getBookingHistory()
	        +checkInGuest()
	        +checkOutGuest()
        }
        class APIEndpoints {
	        +publicRoutes()
	        +authenticatedRoutes()
	        +ownerRoutes()
	        +bookingRoutes()
        }
	}
	namespace BusinessLogicLayer {
        class User {
	        +ID
	        +username
	        +email
	        +password
	        +role: Enum[guest,owner]
	        +created_at
	        +updated_at
	        +validateCredentials()
	        +getBookingHistory()
        }
        class Place {
	        +ID
	        +owner_id
	        +name
	        +location
	        +description
	        +price_per_night
	        +public_rating
	        +availability_calendar
	        +created_at
	        +updated_at
	        +validateOwnership()
	        +checkAvailability()
        }
        class Review {
	        +ID
	        +reviewer_id
	        +type: Enum[place,guest]
	        +target_id
	        +booking_id
	        +rating
	        +comment
	        +created_at
	        +updated_at
	        +validateEligibility()
	        +validateStayCompletion()
        }
        class Amenity {
	        +ID
	        +name
	        +description
	        +category
	        +icon
	        +created_by
	        +created_at
	        +updated_at
	        +validateUniqueness()
        }
        class Booking {
	        +ID
	        +place_id
	        +guest_id
	        +check_in_date
	        +check_out_date
	        +status: Enum[pending,confirmed,completed,cancelled]
	        +total_price
	        +created_at
	        +updated_at
	        +validateDates()
	        +calculatePrice()
        }
	}
	namespace PersistenceLayer {
        class UserRepository {
	        +findByCredentials()
	        +findByRole()
	        +save()
	        +update()
	        +delete()
	        +getBookingHistory()
        }
        class PlaceRepository {
	        +findPublicDetails()
	        +findFullDetails()
	        +findByAmenities()
	        +findAvailable()
	        +save()
	        +update()
	        +delete()
        }
        class ReviewRepository {
	        +findPlaceReviews()
	        +findGuestReviews()
	        +findPublicRatings()
	        +findByBooking()
	        +save()
	        +update()
        }
        class AmenityRepository {
	        +findAll()
	        +findByPlace()
	        +findByCategory()
	        +findPopular()
	        +save()
	        +update()
	        +delete()
        }
        class BookingRepository {
	        +findActiveBookings()
	        +findByDateRange()
	        +findByGuest()
	        +findByPlace()
	        +save()
	        +update()
	        +delete()
        }
        class EntityManager {
	        +executeQuery()
	        +handleTransaction()
	        +trackAudit()
	        +validateRelations()
        }
	}
    APIEndpoints --> UserServices
    APIEndpoints --> PlaceServices
    APIEndpoints --> ReviewServices
    APIEndpoints --> AmenityServices
    APIEndpoints --> BookingServices
    User --> UserRepository
    Place --> PlaceRepository
    Review --> ReviewRepository
    Amenity --> AmenityRepository
    Booking --> BookingRepository
    Place "1" *-- "many" Review
    Place "1" o-- "many" Amenity
    User "1" -- "many" Review
    User "1" -- "many" Place
    Place "1" -- "many" Booking
    User "1" -- "many" Booking
    Booking "1" -- "1" Review
    UserRepository --> EntityManager
    PlaceRepository --> EntityManager
    ReviewRepository --> EntityManager
    AmenityRepository --> EntityManager
    BookingRepository --> EntityManager

```



## Sequence Diagram
### Stories
**userStories**
- [x] As a `user` i want to create an account
    - Click the button `sign-up`
    - New page requesting details of `user`
    - User will fill out form and click `register` to complete
    - New page to confirm email address
    - Once `approved` `user` will be returned back to home page. 

- [ ] As a `owner`(`user`) i want to create a `place`
    - Click `create_place` button
    - Fill out `place_form`
    - Click submit then `place` will be `listed`
     
- [ ] As a `user` i want to submit a `review`
    - Click `submit_review` button after stay date
    - Fill out `review_form` including `rating`
    - Click submit
    - redirected to `place_list` to see their `review`

- [x] As a `user` i want to search for a `place`
    - Click `search_field`
    - Fill in search requirements
    - Click search
    - `place_list` will showcase in "gallery" or on page


- As a `user` i want to delete my `place`
- As a `user` i want to create a `booking`
- As a `user` i want to delete my `account`
- As a `user` i want to update my `details`
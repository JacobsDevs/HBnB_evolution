![alt text](<Airbnb Project.png>)


# HBnB Evolution Technical Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [High-Level Package Diagram](#high-level-diagram)
3. [Business Logic Layer](#class-diagram)
4. [API Interaction Flow](#sequence-diagram)

## Introduction
This technical documentation provides a comprehensive blueprint for the HBnB Evolution application, a simplified version of an AirBnB-like platform. The documentation outlines the systems architecture, detailed design of the business logic, and interactions between different components. 

### Project Scope
The HBnB Evolution application supports:
- User registration and profile management
- Property Listing and management
- Review systems for properties
- Amenity management for properties

## High-Level Diagram
### Package Diagram: 
This diagram illustrates the three-layer architecture of the HBnB application. 

```mermaid

graph TD

    subgraph Persistence Layer
        SQLDB(SQL DB)
    end

    subgraph Business Layer
        subgraph Property
            Place(Place)
            Amenity(Amenity)
            Review(Review)
        end
        Facade(Facade)
        User(User)   
    end

    subgraph Presentation Layer
        UI(UI)
        API(APIs)
    end

```

It is meant to depict a conceptual overview of how the elements of the HBnB system are organized and how they interact with each other.

Follow this *[link](https://app.diagrams.net/#HJacobsDevs%2FHBnB_evolution%2Fokky%2FHBnB%20Evolution%20-%20Package%20Diagram.drawio#%7B%22pageId%22%3A%22b5b7bab2-c9e2-2cf4-8b2a-24fd1a2a6d21%22%7D)* for a more detailed view:

### Layer Responsibilities
##### Presentation Layer

1. Provides user interaction via a UI (User Interface).

2. Exposes system functionalities through APIs.

3. Handles client requests and formats responses accordingly.

##### Business Logic Layer

1. Manages core application logic and data processing.

2. Contains the Facade component, which acts as an interface for various business operations.

3. Handles Users, Properties (Places, Amenities, Reviews), and their interaction with each other.

4. Ensures security, validation, and enforcement of business rules.


##### Persistence Layer

1. Stores and manages data using a SQL Database.

2. Ensures data consistency and integrity.

3. Provides CRUD (Create, Read, Update, Delete) operations for the business layer.

---

## Business Logic Layer
### Class Diagram
```mermaid
classDiagram
    class BaseEntity {
        +UUID id
        +created_at
        +updated_at
    }

    class User {
        +first_name: string
        +last_name: string
        +email: string
        -password: string
        +is_admin: boolean
        +register()method
        +update_profile()method
        +delete_account()method
    }

    class Place {
        +title: string
        +description: string
        +price: float
        +latitude: float
        +longitude: float
        +User: owner
        +List~Amenity~ amenities
        +create() method
        +update() method
        +delete() method
        +list_by_owner() method
    }

    class Review {
        +reviewer: User/UUID
        +place: Place
        +rating: int
        +comment: string
        +create() method
        +update() method
        +delete() method
        +list_by_place() method
    }

    class Amenity {
        +name: string
        +description: string
        +create() method
        +update() method
        +delete() method
        +list_all() method
    }

    BaseEntity <|-- User
    BaseEntity <|-- Place
    BaseEntity <|-- Review
    BaseEntity <|-- Amenity
    
    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : receives
    Place "1" --> "0..*" Amenity : has
```

### Logic Explanation

<details><summary><u>BaseEntity Class</u></summary>
<br>

*This is the abstract base class that provides common attributes for all entities in the system.*

#### Attributes:
- `id` (UUID): Unique identifier for each entity instance
- `created_at` (DateTime): Timestamp when the entity was created
- `updated_at` (DateTime): Timestamp when the entity was last updated

#### Purpose:
- Provides audit trail capabilities
- Ensures consistent identification across all entities
- Implements common functionality for entity tracking
</details>

<details><summary><u>User Class</u></summary>
<br>

*Represents a user in the system, extending BaseEntity.*

#### Attributes:
- `first_name` (String): User's first name
- `last_name` (String): User's last name
- `email` (String): User's email address (unique)
- `password` (String): Hashed password
- `is_admin` (Boolean): Flag indicating administrative privileges

#### Methods:
- `register()`: Creates a new user account
- `update_profile()`: Updates user information
- `delete_account()`: Removes user account from system

#### Relationships:
- **One-to-Many** with Place (as owner)
- **One-to-Many** with Review (as reviewer)
</details>

<details><summary><u>Place Class</u></summary>
<br>

*Represents a property listing in the system, extending BaseEntity.*

#### Attributes:
- `title` (String): Name/title of the property
- `description` (String): Detailed description
- `price` (Float): Daily rental price
- `latitude` (Float): Geographic latitude
- `longitude` (Float): Geographic longitude
- `owner` (User): Reference to the property owner
- `amenities` (List<Amenity>): Associated amenities

#### Methods:
- `create()`: Lists a new property
- `update()`: Modifies property details
- `delete()`: Removes property listing
- `list_by_owner()`: Retrieves all properties for a specific owner

#### Relationships:
- **Many-to-One** with User (as owner)
- **One-to-Many** with Review (as reviewed place)
- **Many-to-Many** with Amenity
</details>

<details><summary><u>Review Class</u></summary>
<br>

*Represents a user review for a property, extending BaseEntity.*

#### Attributes:
- `reviewer` (User): Reference to the user writing the review
- `place` (Place): Reference to the reviewed property
- `rating` (Integer): Numerical rating (typically 1-5)
- `comment` (String): Textual review content

#### Methods:
- `create()`: Submits a new review
- `update()`: Modifies review content
- `delete()`: Removes a review
- `list_by_place()`: Retrieves all reviews for a specific property

#### Relationships:
- **Many-to-One** with User (as reviewer)
- **Many-to-One** with Place (as reviewed property)
</details>

<details><summary><u>Amenity Class</u></summary>
<br>

*Represents a property amenity, extending BaseEntity.*

#### Attributes:
- `name` (String): Name of the amenity
- `description` (String): Detailed description of the amenity

#### Methods:
- `create()`: Adds a new amenity type
- `update()`: Modifies amenity details
- `delete()`: Removes an amenity type
- `list_all()`: Retrieves all available amenities

#### Relationships:
- **Many-to-Many** with Place
</details>

<details><summary><u>Relationship Details</u></summary>

### User --> Place Relationship
- A user can own multiple places
- Each place must have exactly one owner

### User --> Review Relationship
- A user can write multiple reviews
- Each review must have exactly one reviewer

### Place --> Review Relationship
- A place can have multiple reviews
- Each review must be associated with exactly one place

### Place --> Amenity Relationship
- A place can have multiple amenities
- An amenity can be associated with multiple places
</details>

<details><summary><u>Data Validation Rules</u></summary>

### User Entity
- Email must be unique and follow email format
- Password must meet minimum security requirements
- First name and last name cannot be empty

### Place Entity
- Price must be positive
- Title and description cannot be empty
- Must have at list one Amenity attached

### Review Entity
- Rating must be between 1 and 5
- Comment cannot be empty
- User cannot review their own property
- User can only review property they booked

### Amenity Entity
- Name must be unique
- Description cannot be empty
</details>

---

## Sequence Diagram
### User Registration
### Place Creation
### Review Submission
### Place Search


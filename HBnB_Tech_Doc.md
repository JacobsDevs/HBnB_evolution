# HBnB Evolution Technical Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [High-Level Architecture](#high-level-diagram)
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
### Package Diagram
```mermaid```

### Layer Responsibilities
##### Presentation Layer
- 
##### Business Logic Layer
- 
##### Persistence Layer
- 

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
Represents a property listing in the system, extending BaseEntity.

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

---

## Sequence Diagram
### User Registration
### Place Creation
### Review Submission
### Place Search


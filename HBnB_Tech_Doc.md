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



---

## Sequence Diagram
### User Registration
### Place Creation
### Review Submission
### Place Search


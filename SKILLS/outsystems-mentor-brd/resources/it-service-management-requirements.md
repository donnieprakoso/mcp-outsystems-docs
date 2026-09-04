# IT Service Management (ITSM) - Requirements Document

Version: 1.0

Date: August 1, 2025

Author: Product Management

### 1. Application Overview

This document outlines the requirements for an **IT Service Management (ITSM) Help Desk** application. The purpose of this system is to provide a centralized platform for employees to submit IT support requests (tickets), and for the IT team to manage, track, and resolve these tickets efficiently.

### 2. General Application Settings

The application must use the **"Mentor"** theme available in the ODC tenant.

### 3. Data Model

#### Entities & Attributes

* **Entity: Ticket**
  + This entity is stored **locally**.
  + Attributes include:
    - Id: An Identifier that serves as the Primary Key.
    - TicketNumber: Text, an auto-generated, unique ticket identifier.
    - Subject: Text, a brief summary of the issue.
    - Description: Text, a detailed description of the issue.
    - SubmittedDate: DateTime, a timestamp of when the ticket was submitted.
    - CreatedBy: User Identifier, to track the employee who submitted the ticket.
    - AssignedToId: User Identifier, for the IT Agent assigned to the ticket.
    - StatusId: An Identifier that is a Foreign Key to the TicketStatus static entity.
    - CategoryId: An Identifier that is a Foreign Key to the TicketCategory static entity.
* **Entity: Comment**
  + This entity is stored **locally**.
  + Attributes include:
    - Id: An Identifier that serves as the Primary Key.
    - CommentText: Text, the content of the comment.
    - CreatedDate: DateTime, a timestamp for the comment.
    - AuthorId: User Identifier, for the user who wrote the comment.
    - TicketId: An Identifier that is a Foreign Key to the Ticket entity.

#### Entity Relationships

* A **Ticket** can have many **Comments** (One-to-Many).

### 4. Static Entities

* **Entity Name:** TicketStatus
  + **Purpose:** To define the possible states of a support ticket.
  + **Records:** New, Assigned, In Progress, Resolved, Closed.
* **Entity Name:** TicketCategory
  + **Purpose:** To categorize the type of IT issue.
  + **Records:** Hardware, Software, Network, Account Access, Other.

### 5. Roles & Permissions

* **Role: Employee**
  + Ticket: Edit Access (Own records only, based on the CreatedBy attribute).
  + Comment: Edit Access (Own records only).
* **Role: IT Agent**
  + Ticket: Edit Access (All records).
  + Comment: Edit Access (All records).
  + **Special Permission:** Can assign tickets to themselves or other IT Agents. Can change the status of any ticket.
* **Role: IT Manager**
  + Ticket: Full Access.
  + Comment: Full Access.
  + **Special Permission:** Can view dashboards and reports on ticket resolution times and agent performance.

### 6. Main Features & Screens

1. **Dashboard:** A landing page for IT Managers showing key metrics like open tickets, average resolution time, and tickets by category. For Employees, it shows a list of their open tickets.
2. **Submit Ticket:** A simple form for Employees to create a new support ticket, requiring a subject, description, and category.
3. **Ticket Queue:** A screen for IT Agents to view a list of all unassigned and open tickets, with filtering and searching capabilities.
4. **Ticket Details:** A screen to view a single ticket's details, including its description, status, assigned agent, and a chronological list of all comments. Users can add new comments on this screen.
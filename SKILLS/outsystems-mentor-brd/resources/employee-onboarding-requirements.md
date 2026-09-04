# Employee Onboarding - Requirements Document

Version: 1.0

Date: August 1, 2025

Author: Product Management

### Application Overview

This document outlines the requirements for an **Employee Onboarding** application. The system will streamline and automate the onboarding process for new hires, ensuring all necessary tasks are completed by the relevant stakeholders (HR, IT, Hiring Manager) in a timely manner.

### General Application Settings

Name my application, “Employee Onboarding System”.

### Data Model

#### Entities & Attributes

* **Entity: New Hire**
  + This entity is stored **locally**.
  + Attributes include:
    - Id: An Identifier that serves as the Primary Key.
    - FullName: Text, the full name of the new employee.
    - Picture: Picture of the new hire.
    - PersonalEmail: Email, the new hire's personal email address.
    - JobTitle: Text, the official job title.
    - StartDate: Date, the employee's official start date.
    - Location: Show which country the new hire is based out of.
    - HiringManagerId: User Identifier, for the manager of the new hire.
    - OnboardingStatusId: An Identifier that is a Foreign Key to the OnboardingStatus static entity.
    - LocationId: An Identifier that is a Foreign Key to the Location entity.
* **Entity: Onboarding Task**
  + This entity is stored **locally**.
  + Attributes include:
    - Id: An Identifier that serves as the Primary Key.
    - TaskName: Text, the name of the task (e.g., "Sign Employment Contract").
    - Description: Text, details about the task.
    - DueDate: Date, the deadline for task completion.
    - IsCompleted: Boolean, to track if the task is done.
    - NewHireId: An Identifier that is a Foreign Key to the NewHire entity.
    - AssignedDeptId: An Identifier that is a Foreign Key to the Department static entity.
* **Entity: Location**
  + This entity is stored locally
  + Attributes include:
    - Country Name: Text, name of the country where the new hire is based out of.
    - Address: Text, address of the new hire
    - Postal Code: Text, postal code of the new hire
    - Office Name: (Text) A friendly name for the location.
    - City: (Text) The city where the office is located.
    - State/Province: (Text) The state, province, or region, which is essential for many countries.
    - Country Code: (Text) A standardized two-letter country code (e.g., US, NL, DE) for easier data integration.
    - Time Zone: (Text) The official time zone for the location (e.g., "CET," "PST") to help coordinate tasks across regions.
* **Entity: Document**
  + This entity is stored locally
  + Attributes include:
    - Id: An Identifier that is the Primary Key from the external system.
    - DocumentName: Text, the name of the document.
    - Status: Text, the signing status (e.g., "Sent", "Completed").
    - NewHireId: An Identifier that links the document to the new hire.
    - DateCompleted: (Date/Time) The date and time when all parties successfully signed and completed the document.
    - ExpirationDate: (Date/Time) The deadline by which the document must be signed, if applicable.
    - IsRequired: (Boolean) A flag to indicate if the document is mandatory for the onboarding to be considered complete.

#### Entity Relationships

* A **NewHire** can have many **OnboardingTasks** (One-to-Many).
* A **NewHire** can have many **Documents** (One-to-Many).

### Static Entities

* **Entity Name:** OnboardingStatus
  + **Purpose:** To track the overall progress of a new hire's onboarding.
  + **Records:** Pre-boarding, Day 1, Week 1, Completed.
* **Entity Name:** Department
  + **Purpose:** To assign tasks to the correct department.
  + **Records:** HR, IT, Hiring Manager, New Hire.

### Roles & Permissions

* **Role: HR Specialist**
  + New Hire: Full Access.
  + OnboardingTask: Full Access.
  + Document: View Access.
  + **Special Permission:** Can initiate the onboarding process for a new hire.
* **Role: Hiring Manager**
  + NewHire: View Access (Own team members only).
  + OnboardingTask: Edit Access (Only for tasks assigned to the 'Hiring Manager' department for their new hires).
* **Role: IT Specialist**
  + NewHire: View Access.
  + OnboardingTask: Edit Access (Only for tasks assigned to the 'IT' department).
* **Role: New Hire**
  + NewHire: View Access (Own record only).
  + OnboardingTask: Edit Access (Only for tasks assigned to the 'New Hire' department).
  + Document: View Access (Own documents only).

### Main Features & Screens

* List screen of locations with map view to be displayed to show the employee location.
* List screen of new hires to be displayed as a gallery.
* List screen of onboarding tasks should be displayed as master detail.
* List screen of documents should be displayed as a card list.
* Dashboard should consist of below visuals:
  + Total Active Onboardings as a counter
  + Pending Tasks as a counter
  + Average Onboarding Completion Time as Counter
  + Overdue Tasks by Department as a horizontal bar chart
  + New Hires by Onboarding Status as Donut Chart
  + Document Status Breakdown as a Pie Chart
  + Total tasks by department as a pie chart
  + Hiring by Location as vertical bar chart
  + New Hires with Pending Tasks as List
  + Do not add anything else besides these charts that are mentioned. Make sure there are no lists displayed on the dashboard.
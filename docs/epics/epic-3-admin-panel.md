# Epic: Admin Panel

### **1. Name of the Epic: Admin Panel**

### **2. Description / Overview**

This epic encompasses all administrative capabilities required to manage elections, candidates, voters, and global settings from a centralized interface. It provides the tools needed by election administrators to configure, control, and monitor elections within the platform, ensuring a secure, flexible, and easy-to-use backend for managing the entire voting lifecycle.

The Admin Panel is intended for authenticated users with admin roles and plays a vital role in setting up elections, controlling access, managing participants, and ensuring the integrity and control of the system.

### **3. Goal / Objective**

* Allow admins to create and configure elections with clear start and end periods.
* Enable easy management of candidates and their associated profiles.
* Support manual or bulk voter registration with validation mechanisms.
* Provide control over election visibility and participation.
* Maintain administrative authority over key election settings and status.


### **4. Definition of Done for the Epic**

* Admins can create, update, and delete elections with proper time and metadata fields.
* Candidate profiles (name, photo, manifesto) are managed through a secure form.
* Admins can add or remove voters through Database Manipulation.
* Compiles with ACID principle.
* Admins can pause or resume ongoing elections using a secure toggle.
* Only authorized admin users can access this panel.
* Full audit logs are captured for every admin action performed.

### **5. Associated User Stories**

###3.1 * [User Story: Create/Edit/Delete Elections]
  - Admin can create elections with metadata like name, start/end time, and description.
  - Admin can update or delete existing elections before the voting period begins.

###3.2 * [User Story: Add/Edit/Delete Candidates]
  - Admin can add candidates with associated information such as photos, names, departments, and manifestos, past achievements.
  - Existing candidates can be updated or removed securely.

###3.3 * [User Story: Add/Remove Voters]
  - Admin can manually register or remove voters from the election roster.

### 3.4 * [User Story: Import Voter Database file]
  - Admin can upload a database file containing the voters list.
  - System checks file structure, duplicates, and errors before processing.

###3.5 * [User Story: Enable/Disable Voting]
  - Admin has a control to toggle voting on or off per election.
  - This action is tracked and reflected in the system state.

### **6. Dependencies**

* **Requires:** Epic: Authentication & Access (admin login and role-based access control).
* **Required by:** Epic: Results and Transparency (only after elections are created).

### **7. Out of Scope.**

### **9. Notes / Discussion / Changelog**

#### Notes:

#### Changelog:


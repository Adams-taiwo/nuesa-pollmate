# Epic: Authentication & Access Control

### **1. Name of the Epic: Authentication & Access Control**


### **2. Description / Overview**

This epic establishes the foundational security infrastructure for the e-voting platform. It focuses on enabling secure authentication methods for both voters and administrators, enforcing proper access permissions based on user roles, and maintaining secure sessions using JSON Web Tokens.

The goal is to ensure that only authorized users can access the system, interact with appropriate features, and maintain the integrity and confidentiality of the platform.

This functionality is essential for all users of the platform — voters who need a secure and simple way to log in using their voter ID or token, and administrators who manage the backend of elections.

### **3. Goal / Objective**

- Ensure secure login mechanisms for both voters and administrators using their student ID and their Matric No.
- Enforce strict access controls based on user roles and maintain sessions through JWT.
- Prevent unauthorized access or role manipulation.


### **4. Definition of Done**

- Voters can successfully log in using a unique ID/token and receive a JWT.
- Admins can log in with their student ID and matric number to access the admin dashboard.
- All routes are protected using JWT-based authentication.
- Middleware enforces role-based access control.
- Tokens expire and refresh mechanisms are working as expected.



### **5. Associated User Stories**

1.1 **[User Story: Voter Login via Token or ID]**
  - Voters should be able to log in using a unique identifier (voter ID or token).
  - Validate the token against the database.
  - If valid, issue a secure JWT and allow access.

1.2 **[User Story: Admin Login (Student ID/Matric No.)]**
  - Implement a login form with admin credentials.
  - Validate credentials securely using hashed passwords.
  - Redirect to the admin dashboard on success.

1.3 **[User Story: Role-Based Access Control]**
  - Differentiate access based on roles: voter vs admin.
  - Prevent role spoofing via middleware or decorators.

1.4 **[User Story: JWT-Based Secure Session]**
  - Integrate JWT-based authentication across all protected routes.
  - Include token refresh and expiration handling.

---

### **6. Dependencies**

- **Requires:**
  - Database schema for users with role metadata.
  - Password hashing and token generation utility functions.

- **Required by:**
  - Epic: Voting System (users must be authenticated before voting).
  - Epic: Admin Panel (admin features must be protected).

---

### **7. Out of Scope**

- OAuth, biometric, or third-party login integration.
- Multi-factor authentication (to be considered post-MVP).
- Real-time session monitoring/dashboard.

---

### **8. Metrics / Success Measurement**

- **Security:** 100% of protected routes require a valid JWT token.
- **Access Integrity:** 0 unauthorized access attempts allowed past middleware.
- **Login Performance:** Authentication completes within 1 second for 95% of users.
- **Session Validity:** Token expiry and refresh system works without session leaks.

---

### **9. Notes / Discussion / Changelog**

#### Notes:

- Tokens should follow secure signing practices (e.g., HMAC SHA256).
- Refresh tokens should be stored securely in the backend.
- Use `fastapi.security` for implementation of dependency injection in route protection.

#### Changelog:

- **2025-07-30:** Example: Initial version created based on merged PRD feature list.


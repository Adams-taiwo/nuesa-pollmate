# Epic: Frontend UI/UX

### **1.  Name of the Epic: Frontend UI/UX**


### **2. Description / Overview**

This epic focuses on delivering a responsive, accessible, and user-friendly interface for all users (voters and administrators). The goal is to ensure users can intuitively navigate the platform, perform necessary actions, and receive clear visual feedback, regardless of device or technical ability.

A clean and inclusive interface is essential for building trust and ensuring high voter turnout.

### **3. Goal / Objective**

* Provide clear, minimal, and attractive UI layouts for all voter and admin interactions.
* Visualize important information (ballot options, voting status, results) in a digestible manner.
* Offer accessible design patterns for users with disabilities.
* Incorporate visual feedback for all interactions to guide users effectively.

### **4. Definition of Done for the Epic**
* The homepage clearly presents entry points for “Log In” and “Vote Now,” with intuitive calls-to-action.
* The Log In / Authentication page provides a form for Student ID and Matriculation Number, complete with input validation, error messages, and “Forgot ID” assistance.
* The dashboard cleanly displays active elections the user is eligible to vote in, showing titles and open/close status.
* The election details page presents the election name, opening and closing times, and a summary of positions before the ballot.
* The ballot page clearly displays each candidate’s name, photo, manifesto, and past accomplishments for every position, with single‐selection controls.
* The vote confirmation screen or modal prompts users to review their selections, then shows a success message and a unique transaction ID/hash for auditability.
* The results page presents real-time vote counts during the election and finalized, per-candidate breakdowns post–election.
* The admin dashboard offers navigation to Elections, Candidates, Voters, and Settings, plus live metrics (turnout %, vote distribution, audit log summaries).
* All interactive flows (login, ballot submission, form actions) include visible loading states, and users receive clear success/error feedback via toast notifications or alerts.
* The “How to Vote” page provides step-by-step text instructions alongside visual diagrams or videos.
* A full set of error pages should be implemented:
•	400 Bad Request
•	403 Forbidden
•	404 Not Found
•	500 Internal Server Error
* The application meets accessibility standards, including keyboard navigation, screen-reader support, sufficient color contrast, and meaningful alt text for all images.

### **5. Associated User Stories**

4.1 * [User Story: Access and Login Flow]
Identity is authenticated using Student ID and Matriculation Number, with validation and error handling.

4.2 * [User Story: View Available Elections]
After login, users land on a dashboard showing active elections they’re eligible for with each election displays its title and open/close status.

4.3 * [User Story: View Election Details]
Upon selecting an election, users see its name, opening/closing times, and summary of positions before accessing the ballot.

4.4 * [User Story: Browse Candidate Profiles & Cast Vote]
Users can view candidates grouped by position, each with photo, name, manifesto, and accomplishments. Users make their selection for each position.

4.5 * [User Story: Confirm Vote Submission]
Before finalizing, users review their choices on a confirmation screen or modal. Upon confirmation, they receive a success message and a unique transaction ID/hash.

4.6 * [User Story: Receive Vote Confirmation & Audit Token]
After submitting, users see a confirmation message indicating their vote was cast successfully. A transaction ID or hash is displayed to support auditability without revealing choices.

4.7 * [User Story: Results Display]
The results page shows real-time vote counts during the election. After close, it presents finalized per-candidate breakdowns and totals.

4.8 * [User Story: Admin Dashboard Design]
Admins access a dashboard with navigation to Elections, Candidates, Voters, and Settings. Live metrics (turnout %, vote distribution, audit logs) are prominently displayed.

4.9 * [User Story: UI Feedback & Loading States]
All form actions include visible loading indicators. Users receive clear success and error notifications (toasts or alerts).

4.10 * [User Story: How to Vote Guidance]
A dedicated “How to Vote” page offers clear text instructions and visual aids (diagrams or videos).

4.11 * [User Story: Error Page Handling]
Standard error pages are implemented for 400, 403, 404, and 500 HTTP statuses.

### **6. Dependencies**
* **Requires:** Epic: Voting System (for ballot functionality), Epic: Results and Transparency (for result components).
* **Required by:** None directly, but critical to overall user engagement and usability.

### **7. Out of Scope**

### **9. Notes / Discussion / Changelog**

#### Notes:

#### Changelog:

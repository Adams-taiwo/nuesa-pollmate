# Epic 2

### **1. Name of the Epic: Voting System**

### **2. Description / Overview**

This epic encapsulates the core functionality that enables voters to participate in elections on the platform. It includes all backend and frontend logic required to display ongoing elections, render candidate ballots, ensure eligibility, and allow secure vote submission. 

The goal is to create a seamless and secure voting experience for authenticated users, ensuring integrity through rules such as one vote per user and strict voting periods. This functionality is crucial for delivering the primary value of the system—electronic voting—and is targeted at authenticated voters participating in elections on the platform.

### **3. Goal / Objective**

* Allow authenticated users to cast a vote in one or more active elections securely.
* Display real-time, valid voting options (only elections the user can vote in).
* Prevent duplicate voting and ensure strict voting windows.
* Confirm vote submission to users for transparency and trust.



### **4. Definition of Done (for the Epic)**

* Eligible users can see and access only ongoing elections.
* Ballots are rendered correctly with candidate information.
* The system enforces one vote per user per election.
* Voting access is locked before the start time and after end time.
* Users receive a clear confirmation after successfully casting their vote.

### **5. Associated User Stories**

#### 2.1 [User Story: Display Active Elections]
- Only elections within the configured start and end time should be listed.
- Each election card should include title, description, position being contested, and end time.
- Inactive or upcoming elections should not be shown.
- Frontend must pull data dynamically using API or WebSocket updates.

#### 2.2 [User Story: Show Candidates in Ballot Format]
- Candidates are displayed with name, photo (if available), and a short bio/manifesto.
- Users can select only one candidate per position.
- The layout should mimic real-world ballots for usability and familiarity.
- Candidate order can be randomized per session to prevent bias.

#### 2.3 [User Story: Enforce One-Vote-Per-User]
- Once a vote is submitted, the system stores it and marks the voter as having voted.
- Any attempt to re-submit a vote results in a clear error message.
- Backend validates vote submissions and prevents duplication through database constraints or logic.
- Audit logs capture voter ID and timestamp for every valid vote.

#### 2.4 [User Story: Voting Period Enforcement]
**Acceptance Criteria:**
- The backend checks current server time against election start and end timestamps before accepting votes.
- If a vote is attempted outside the allowed period, an appropriate error is returned to the frontend.
- The voting button or interface is disabled for ineligible periods on the frontend.
- Election status is updated in real-time using WebSockets or periodic polling.

#### 2.5 [User Story: Vote Submission Confirmation]
- After a successful vote, display a confirmation screen with the candidate chosen and timestamp.
- A success toast or modal popup is shown to the user.
- Backend returns a 200 OK response with vote receipt data (non-sensitive).

### **6. Dependencies**

* **Requires:** 
  * Completion of Epic: Authentication & Access (users must be logged in and verified to vote).
  * Backend DB schema to support election, user, and vote tracking.

* **Required by:**  
  * Epic: Results and Transparency (vote count and final result depend on vote submissions).
  * Epic: Admin Panel (election creation and start/end configuration).


### **7. Out of Scope**

* Vote encryption for end-to-end anonymization.
* Complex voting systems like multi-round voting.


### **8. Metrics / Success Measurement**

* **Accuracy:** 0% duplicate voting instances in logs.
* **Engagement:** % of eligible voters who cast at least one vote per election.
* **Completion:** >98% of vote attempts result in successful confirmation.
* **Timeliness:** >99% of votes cast within the defined voting period boundaries.


### **9. Notes / Discussion / Changelog**

#### Notes:

#### Changelog:

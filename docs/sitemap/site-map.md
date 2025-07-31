USER SITEMAP

+-----------------------------------+
| Access e-voting site homepage     |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Select “Log In” |
+-----------------------------------+
                 |	
                 V
+-----------------------------------+
| Log In / Authentication Page      |
| – Enter Student ID & Matric No.   |
| – Input validation & error states |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Authenticate Identity             |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| View Dashboard                    |
| (List of active elections user    |
|  is eligible to vote in)          |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| View Election Details             |
| – Election name                   |
| – Opening & closing times         |
| – Positions summary               |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Ballot Page                       |
| – Browse candidates by position   |
| – Candidate info: photo, name,    |
|   manifesto, accomplishments      |
| – Single-selection controls       |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Review & Confirm Selections       |
| (Confirmation screen/modal)       |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Receive Vote Confirmation         |
| – Success message                 |
| – Transaction ID / audit hash     |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| **Error Pages**                   |
| – 400 Bad Request                 |
| – 403 Forbidden                   |
| – 404 Not Found                   |
| – 500 Internal Server Error       |
+-----------------------------------+
Voter Flow:
1.	Logs in with unique ID/token
2.	Sees a list of ongoing elections
3.	Selects an election
4.	Views candidate list and casts a vote
5.	Sees confirmation page and is locked out from voting again

ADMINS SITEMAP

+-----------------------------------+
| Access e-Voting Admin Homepage    |
| (via web browser)                 |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Select “Log In”                   |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Log In / Authentication Page      |
| – Enter Admin ID & Password       |
| – Input validation & error states |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Authenticate Identity             |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Admin Dashboard                   |
| – Overview: turnout %, vote dist. |
| – Nav links: Elections,           |
|   Candidates, Voters, Audit Logs, |
|   Settings                        |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Manage Elections                  |
| – List all elections              |
| – Create / Edit / Delete          |
| – Define name, times, positions   |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Manage Candidates                 |
| – List candidates by election     |
| – Add / Edit / Remove             |
| – Upload photo, manifesto, bio    |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Manage Voters                     |
| – View eligible voter list        |
| – Upload / Import voter records   |
| – Activate / Deactivate accounts  |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| View Audit Logs                   |
| – Search by transaction ID / date |
| – Filter by election or user      |
| – Download log exports            |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| Settings                          |
| – Configure site parameters       |
| – Manage admin accounts           |
| – Accessibility & UI options      |
+-----------------------------------+
                 |
                 V
+-----------------------------------+
| **Error Pages**                   |
| – 400 Bad Request                 |
| – 403 Forbidden                   |
| – 404 Not Found                   |
| – 500 Internal Server Error       |
+-----------------------------------+


Admin Flow:
1.	Logs in via admin credentials
2.	Creates a new election with title, date range
3.	Adds candidates to the election
4.	Uploads or manages voter list
5.	Monitors voter turnout and real-time results
6.	Ends the election and publishes final results
7.	Review system logs



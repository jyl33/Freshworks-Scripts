- The ticket property txt files are designed for an IT use case, edit them as you please!


- To run this script, open your terminal and navigate to the autoTicketSubmit folder and run 'python populatefs.py' or 'python populatefd.py'


- This script requires the requests library. Install using 'pip install requests'.
	If you don't have pip, run these commands:
	
		1. curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		2. python get-pip.py
		3. pip install requests



- make sure to have no blank lines in your txt files, this will result in an indexOutOfBounds error. If you're getting this error, check the referenced file and delete any lines with no text.


- To populate custom fields:

	Add a 'custom_field' section
	'{ "helpdesk_ticket":{"description":"WiFi Down"..."source": 2 **, "custom_field": { "type_194465": "L1", "how_long_have_you_had_this_issue_194465":"Less than a day"}**} }'  
	(Ex: 2 custom fields named "type" and "how long have you had this issue?")
	
	To find the exact name for the field:
		
		1. Install the Json Viewer Chrome extension https://chrome.google.com/webstore/detail/json-viewer/gbmdgpbipfallnflgajpaliibnhdgobh?hl=en-US
		2. go to https://domain.freshservice.com/helpdesk/tickets.json
		3. Search for the custom field name

- To change frequency and number of tickets submitted:
	This can be edited in the auto_submit() function.
	Find the function and there are comments with instructions on how to edit the values
	
- If all of your tickets are being assigned low priority, turn off the Priority Matrix

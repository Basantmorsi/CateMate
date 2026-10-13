Create a backend endpoint for logged-in pet owners to view their profile's information
The pet owner profile should show the following fields: 
name
gender(if given while registration)
age (if given while registration)
which city he has in his address 
email
phone number(if given while registration)
bio (if given while registration)
which gender does he prefer to receive messages from if selected at registration
a list of registered pets when exists, 
a button linked to a separate endpoint to add new pet


The endpoint should not show the pet owner's password but will have an option to change it (will be a separate endpoint)
The endpoint will not add new pets or delete existing ones

The pet owner must be logged-in to be able to view his profile page and should not access other users' profiles

Given the user is logged-in in the website
When he clicks on his name 
Then he can view all related infos about him

Given the user is logged-out 
When he enters the /me endpoint 
Then he gets access forbidden message 
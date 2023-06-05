# Data Engineering Exercise
Design and implement a data pipeline that that pulls data from [Open Library](https://openlibrary.org/developers/api) for a specific subject you are interested in. The [subjects API](https://openlibrary.org/dev/docs/api/subjects) can help you find a list of authors and books related to a particular subject. We recommend you keep the number of books you pull between 100 and 1000. As an output of this exercise we expect to see a minimum of the following:

1. An architecture and the technologies or services you would use during implementation.
2. Python program that pulls data from the rest api
3. CSV files for the following:
	* Authors
	* Books
	* Authors and Books (a bridge table between the previous entities)
4. DDL to create a hypothetical database schema ( you don't have to create a DB but you are welcome to)

The objective of this exercise is to have you walk us through a solution you have created. Do as much or as little as you would like. 

*NOTE: Keep in mind that this is meant for a roughly 60 minute interview and we want to understand your thinking and process. If you leave something out for the sake of time, mention it during your presentation. Mention things you would improve if this was a production grade applicaiton.*

## ReadMe
Please include:
* a readme file that explains your thinking
* a data model showing your design, explain why you designed the db and include the DDL used to generate the tables in your database
* how to run and set up your project
* if you have tests, include instructions on how to run them
* a description of:
	* enhancements you might make
	* additional features you have added to help or that you found interesting
* questions you have
* recommendations for us


## Additional Info:
* we expect that this will take you a few hours to complete
* use any language or framework you are comfortable with, we prefer Python
* AWS is our cloud provider please include mention of the services you would choose
* Bonus points for including terraform or any other infrastructure as code
* Bonus points for security, specs, tests etc.
* Do as little or as much as you like.

Please fork this repo and commit your code into that fork. Show your work and process through those commits.

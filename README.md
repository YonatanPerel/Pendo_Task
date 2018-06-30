# Pendo_Task

instractions:

run on a virtual env, with requierments.txt installed.

	create user:
		POST {'username': username,
			'password': password}
		to: /signup
	

	create new blog post:
		POST {'content': content} + HTTP basic authentication details.
		to: /entry
	
	
	get most upvoted list:
		GET /entry
		this gives you the list from the most voted cache table witout accessing the main posts table.
		the cache is updated on a schedual to keep up to date, and with every upvote(if necessery)
	

	get a blog post:
		GET /entry/post_id
	

	update blog post:
		POST {'content': content OR 'upvote': true/false} + HTTP basic authentication details.
		to: /entry/post_id
		this is used for both updating the content of the post, and up/downvoting it, and therefore only needs one of the parameters.
	
	
	Delete blog post:
		DELETE /entry/post_id + HTTP basic authentication details.
	

	
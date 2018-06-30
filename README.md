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
	

	get a blog post:
		GET /entry/post_id
	

	update blog post:
		POST {'content': content OR 'upvote': true/false} + HTTP basic authentication details.
		to: /entry/post_id
		this is used for both updating the content of the post, and up/downvoting it, and therefore only needs one of the parameters.
	
	
	Delete blog post:
		DELETE /entry/post_id + HTTP basic authentication details.
	

	
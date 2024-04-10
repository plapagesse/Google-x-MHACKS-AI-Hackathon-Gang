# HACKATHON IDEAS:

1. Open source projects mailing list tracker (sentiment analys-isish?) 
	- inspiration: https://robmensching.com/blog/posts/2024/03/30/a-microcosm-of-the-interactions-in-open-source-projects/	
		- given recent xz attack - hacker took maintainer's role since original maintainer was burnt out and being pressured by contributors
		- if there was a way for central authorities to flag maintainers in need of support, could have been prevented 
		- Could use gemini's large context window for: 
			- flagging messages 
			- summarize struggles/issues maintainer is going through (giving proof - pointing to specific messages)
			- classify the problem (too much too handle, mental health down, etc) - could influence solution
			- calculate risk score based on the number of flagged messages (not gemini, but we can use the number of flagged messages to do so)
		- Enable central maintainer (linus and his team xd) to track and suface risk across projects

1.  Given analysis, search research papers/academia/books for accurate evidence/summaries 

1. Study Assistant - real time quizzing/knowledge checkin while watching lecture, exam prep, practice questions, conceptual diagramming
		- create personalized learning paths, adjust based on student responses/performance, based on piazza posts too ? ? ?idk
		- create study guides based on lectures
		- student can ask "how to learn more about [TOPIC]" and we can tell them exact timestamp in video to look at, and exact practice problems to do, and give more maybe

1.  Editing video footage ? 

1. Company specific interview prep package? idk idk might already be done?? or too basic?? lol
	- using all common interview questions, from leetcode, glassdoor, advice from reddit?, company website, application, youtube videos, tells u what to focus on idk
	- gives mock interview/feedback?  ?? ? ?  

1. test case generator ? ? ? based on large code base and stuff from online related to ur code?? 

1. Intelligent language learning tutor
	- Allows user the opportunity to specify their desired subject material (e.g., "I want to practice talking about the zoo in Spanish")
	- Assuming access to Imagen, we might support augmenting learning via images, e.g., matching generated captions to corresponding pictures, posing questions about content of pictures, etc.
	- Perhaps the LLM could "explain the error" when the user makes a semantic or grammatical mistake

1. Fiction writing assitant / wizard - semi-structured process to help break writers block
	- Interactive question-answer based generation of characters, plot points, settings, etc.
	- Dynamic creation of character portraits
	- Intelligently suggest relationships or conflicts between characters
	- Generate candidate relationship and conflict graphs for inspiration 

1. Event planning wizard
	- semi structured system for planning a Christmas / Birthday / Baby Shower / Wedding / whatever
	- question-answer facilitated generation of
		- invitation text and art
		- meal suggestions
		- event activities, customized to attendee needs and preferences
	- capacity planning assistant 
		- assisted food purchase calculations; "how much pizza should I order?"
			- bucket guests into heavy, moderate, or light eaters
		- what if I have guests with dietary restrictions?
	- potential optimization problem: design seating arrangements that keeps people who don't get along maximally separated 

1. Auto image collage
	- Allow the user to upload a set of images and specify a theme
	- Interpret images to automatically provide captions consistent with a user-specified theme (should support post hoc editing)
		- Intelligently select subsets of images warranting captioning
	- Automatically arrange the images in a visually pleasing manner according to specified constraints / objectives, e.g.
		- images cannot be smaller than size X
		- images can / cannot overlap
		- captions can / cannot overlap images
		- max / min number of objects per page
		- desired caption verbosity
	- Example application: early childhood educators

1. Intelligent meal planning assistant
	- Support uploading an image of ingredients to get meal suggestions
	- Can store contextual information about the user, e.g.,
		- dietary restrictions
		- fitness goals
		- time-of-day (is this likely lunch, breakfast, dinner) 
	- Maybe user can Opt-in to having the bot shame their bad choices
	- User can store long-term feedback / rules ("I prefer mild heat") in an editable knowledge base
	- Upload an image to "how can I make this?" feature

1. PR review assitant
	- Analyze PR diffs to highlight and prioritize the most interesting changes
	- Provide intelligent summaries of code changes ("This PR appears to add several HTTP endpoints")
	- Flag common code issues ("this class appears to violate the Single Responsibility Principle because...")
	- Attempt to intelligently diagnose and explain test case failures


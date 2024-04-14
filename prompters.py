import google.generativeai as genai

from video import get_timestamp, make_request


class FutureTaskPrompter:
    PROMPT = (
        "Note down action items, todos, and follow up tasks required of participants"
        "in this meeting in a single list of succinct bullet points."
        "Don't be wordy - these should be easily imported into"
        "task management software"
    )

    def __init__(self, model):
        self.model = model

    def prompt(self, frames, audio):
        prompt = [self.PROMPT] + frames + [audio]
        response = self.model.generate_content(prompt, request_options={"timeout": 600})
        return response.text


class MeetingEffortPrompter:
    def __init__(self):
        pass

    def prompt(self, frames, audio):
        prompt = """You have been provided with timestamped image frames and an audio recording of a recent meeting. Analyze the content and the conversation to evaluate if every member showed genuine preparation, technical knowledge(not asking clueless and repetitive questions), interest to have defined follow-up tasks, shows up on time for meeting. If even one person demonstrates a lack of either of those, note that in a general sense--don't name people by their names.  """
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        request = make_request(prompt, frames)
        request.append(audio)
        response = model.generate_content(request, request_options={"timeout": 600})
        return response


class MeetingParticipationPrompter:
    def __init__(self):
        pass

    def prompt(self, frames, audio, speaker_frequencies):
        prompt = """You have been provided with timestamped image frames and an audio file of a recent meeting, speaker frequency dictionary and speaker timestamps. Conduct an analysis of overall participation in the meeting. Consider the following:

Assessment of Speaking Time:

Review the total speaking time for each participant as indicated by the speaker frequency dictionary. Identify if some people dominated the conversation excessively more due to significant discrepancies in speaking time among participants.
Role-Based Insights:

Consider the roles of the speakers (e.g., manager, student, staff). Discuss whether the distribution of speaking time seems appropriate based on their roles. Mention if the primary speaker was a manager and if their level of participation was suitable.
Equality of Participation Among Non-Managers:

Specifically assess how non-managerial participants engaged in the conversation. Identify if there were any individuals who were particularly quiet or disproportionately vocal. Stay general about the participation.
Recommendations for Participation Balance:

Suggest practical ways to ensure a more balanced and inclusive participation in future meetings, particularly for those who were less engaged.
Please provide a concise summary of your findings and recommendations to enhance participation equality and meeting effectiveness."""
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        request = make_request(prompt, frames)
        request.append(audio)
        request.append(str(speaker_frequencies))
        response = model.generate_content(request, request_options={"timeout": 600})
        return response


class MeetingProfessionalismPrompter:
    def __init__(self):
        pass

    def prompt(self, frames, audio):
        prompt = """You have been provided with timestamped image frames and an audio recording of a recent meeting. Rate the meeting and speech professsionalism and eloquence, mostly in terms of speech and ways of talking. Observe the language and tone used by participants throughout the meeting. Note very excessive instances of casual or unprofessional language such as 'like', 'um', or other non-professional thing, but don't be too strict. Keep it general, avoid specific names."""
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        request = make_request(prompt, frames)
        request.append(audio)
        response = model.generate_content(request, request_options={"timeout": 600})
        return response


class MeetingRespectPrompter:
    def __init__(self):
        pass

    def prompt(self, frames, audio):
        prompt = """You have been provided with timestamped image frames and an audio file of a recent meeting. Closely monitor interactions among participants to identify clear instances of interruptions or rudeness, or abrupt cutting off. Pay particular attention to tone of voice, how participants handle interruptions, and the nature of disagreements. Highlight significant interactions that demonstrate obvious disrespect or disruption to the flow of conversation.Provide examples of these interactions and suggest how they might be addressed in future meetings."""
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        request = make_request(prompt, frames)
        request.append(audio)
        response = model.generate_content(request, request_options={"timeout": 600})
        return response


class MeetingProductivityPrompter:
    def __init__(self):
        pass

    def prompt(self, frames, audio, speaker_frequencies):
        prompt = "You have been provided with timestamped image frames and an audio file of a recent meeting, along with a dictionary detailing speaker frequencies. Analyze the content of the discussion to determine the proportion of time spent on relevant versus unrelated topics. Identify and quantify moments where the discussion veers off-topic to assess overall meeting productivity in percentages."
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        request = make_request(prompt, frames)
        request.append(audio)
        request.append(str(speaker_frequencies))
        response = model.generate_content(request, request_options={"timeout": 600})
        return response


class MeetingScribePrompter:
    def __init__(self):
        pass

    def prompt(self, frames, audio, attendees):

        attendance = ""
        for person in attendees:
            attendance += person + ", "

        attendance = "ATTENDEES: " + attendance
        print(attendance)

        question = """You are the meeting scribe. Your job is to take 
        detailed notes on what was discussed throughout the meeting. 
        Provide references to time frames of the video when possible.
        The scribe is the person responsible for taking notes during the meeting."""

        context = [question, attendance]

        for frame in frames:
            time_stamp = get_timestamp(frame.display_name)
            context.append(time_stamp)
            context.append(frame)

        context.append(audio)

        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        response = model.generate_content(context, request_options={"timeout": 600})
        print(response.text)

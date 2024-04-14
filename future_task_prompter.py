class FutureTaskPrompter:
    PROMPT = ("Note down action items, todos, and follow up tasks"
              "in this meeting in the form of succinct bullet points."
              "Don't be wordy.")

    def __init__(self, model):
        self.model = model

    def prompt(self, frames, audio):
        prompt = [self.PROMPT] + frames + [audio]
        return self.model.generate_content(prompt, request_options={"timeout": 600})

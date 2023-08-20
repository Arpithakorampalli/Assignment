class LLMWrapper:
    def __init__(self, model, max_tokens, rate_limit_threshold):
        self.model = model
        self.max_tokens = max_tokens
        self.rate_limit_threshold = rate_limit_threshold
        self.conversation_history = []

    def _format_prompt(self, prompt, variables):
        for var_name, var_value in variables.items():
            prompt = prompt.replace(f"{{{var_name}}}", str(var_value))
        return prompt

    def _handle_rate_limit(self):
        # Implement your rate limit handling logic here
        pass

    def _pipeline_to_llm(self, prompt):
        try:
            response = self.model.generate(prompt, max_tokens=self.max_tokens)
            return response
        except RateLimitError:
            self._handle_rate_limit()
            return self._pipeline_to_llm(prompt)

    def add_user_input(self, user_input, variables=None):
        if variables is None:
            variables = {}
        
        formatted_prompt = self._format_prompt(user_input, variables)
        response = self._pipeline_to_llm(formatted_prompt)
        
        self.conversation_history.append((formatted_prompt, response))
        
        return response

    def get_conversation_history(self):
        return self.conversation_history

# Example usage
if __name__ == "__main__":
    class YourLanguageModel:
        def generate(self, prompt, max_tokens):
            # Replace this with your actual model generation logic
            return f"Model response for '{prompt}'"

    # Initialize your language model
    model = YourLanguageModel()

    # Create LLMWrapper instance
    wrapper = LLMWrapper(model, max_tokens=100, rate_limit_threshold=3)

    # Simulate a conversation
    user_input1 = "Hello, can you help me with a math problem?"
    user_input2 = "Sure! What's the problem?"
    user_input3 = "I need to calculate the integral of x^2 dx."

    conversation_variables = {"user_name": "Rajbir", "problem_type": "math"}

    wrapper.add_user_input(user_input1)
    wrapper.add_user_input(user_input2)
    wrapper.add_user_input(user_input3, conversation_variables)

    history = wrapper.get_conversation_history()
    for prompt, response in history:
        print("User:", prompt)
        print("Model:", response)

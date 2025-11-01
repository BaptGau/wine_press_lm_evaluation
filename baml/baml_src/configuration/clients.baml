client<llm> GPT5 {
  provider openai-responses
  options {
    model "gpt-5"
    api_key .env.OPENAI_API_KEY
  }
}
import google.generativeai as genai

genai.configure(api_key="AIzaSyAnTzcVO0f2z3ESHZEEMczdBUIwMYVMlnE")

model = genai.GenerativeModel("gemini-1.5-flash-latest")

response = model.generate_content("Hello")

print(response.text)



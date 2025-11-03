# T-Shirts DB QA 👕

A **question-answering tool** for a MySQL T-Shirts database. Ask natural language questions, and the system generates the correct SQL query, executes it, and returns the answer. Built with **LangChain**, **Google Gemini LLM**, and **Streamlit** for a web interface.  

---
**We can try questions like:**
* _"How many white Levi's shirts do we have?"_
* _"What is the total price of all small size T-Shirts?"_
* _"How much revenue will the store generate if all Nike t-shirts are sold today with discount applied?"_
* _"How many large Adidas t-shirts are left in stock?"_
---
<img width="1163" height="258" alt="image" src="https://github.com/user-attachments/assets/4acf9ce8-f5d2-4706-b2c8-4f564c941953" />
<img width="1015" height="655" alt="image" src="https://github.com/user-attachments/assets/a78df7f7-c44c-46a6-9cdf-bb196a5d9f55" />

---

## Features

- Ask questions in natural language about the T-Shirts inventory.  
- Automatically generates SQL queries and executes them safely.
- Uses a few-shot learning agent to map natural language questions to accurate SQL queries.  
- Displays both the **answer** and the **SQL query** used.  
- Supports **few-shot** learning to improve query accuracy.  
- Built with modern LLM tools for real-time database QA.

---

## Tech Stack

- **Python 3.13+**  
- **LangChain** for LLM orchestration and agent creation  
- **Google Gemini LLM** via `langchain-google-genai`
- **HuggingFace Embeddings** and **Chroma** for few-shot example selection
- **Streamlit** for web interface  
- **MySQL** as the database    
- **Dotenv** for environment variables

---

## How it Works

The app uses a **few-shot SQL agent** powered by a large language model (Gemini). 
- The agent receives your question in natural language.
- It searches for similar examples from a few-shot dataset to guide query generation.
- Generates a syntactically correct SQL query.
- Executes the query safely on the database and returns a natural-language answer.
- You can optionally see the SQL query that was executed for transparency.

import streamlit as st
from db_agent import get_few_shot_sql_agent

st.set_page_config(page_title="T-Shirts DB QA 👕", page_icon="👕")
st.title("T-Shirts: Database Q&A 👕")

question = st.text_input("Ask a question about the database:")

if question:
    with st.spinner("🤔 Thinking... please wait"):
        agent = get_few_shot_sql_agent()
    
        response = agent.invoke(
            {"messages": [{"role": "user", "content": question}]}
        )

        final_answer = response["messages"][-1].content

        sql_query = None
        for msg in response["messages"]:
            if isinstance(msg.content, str) and "SELECT" in msg.content.upper():
                sql_query = msg.content
                break

    st.subheader("Answer:")
    st.success(final_answer)

    if sql_query:
        with st.expander("See SQL Query"):
            st.code(sql_query, language="sql")
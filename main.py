import streamlit as st
from db_agent import get_few_shot_sql_agent

st.set_page_config(page_title="T-Shirts DB QA 👕", page_icon="👕")
st.title("T-Shirts: Database Q&A 👕")

question = st.text_input("Ask a question about the database:")


def extract_text_from_response(response):
    last_msg = response["messages"][-1].content
    
    if isinstance(last_msg, list) and len(last_msg) > 0 and isinstance(last_msg[0], dict):
        return last_msg[0].get("text", str(last_msg))
    
    elif isinstance(last_msg, dict):
        return last_msg.get("text", str(last_msg))
    
    return str(last_msg)



if question:
    with st.spinner("🤔 Thinking... please wait"):
        agent = get_few_shot_sql_agent()
    
        response = agent.invoke(
            {"messages": [{"role": "user", "content": question}]}
        )

        # final_answer = response["messages"][-1].content
        final_answer = extract_text_from_response(response)

        sql_query = None
        for msg in response["messages"]:
            content = msg.content
            if isinstance(content, str) and "SELECT" in content.upper():
                sql_query = content
                break

            elif isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict):
                text = content[0].get("text", "")
                if "SELECT" in text.upper():
                    sql_query = text
                    break

    st.subheader("Answer:")
    st.success(final_answer)

    if sql_query:
        with st.expander("See SQL Query"):
            st.code(sql_query, language="sql")
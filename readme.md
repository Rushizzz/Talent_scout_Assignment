### initialize model
llm = ChatGroq(   model_name="llama-3.3-70b-versatile",   temperature=0.7 )

### Pass propmt to API
llm.invoke(propmt)



from load_llm import llm

ans = llm.invoke("tell me a sad story")
print(ans.content)
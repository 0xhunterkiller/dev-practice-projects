# Learning Langgraph

I was following a nice course on langgraph, with exercises and everything. Uploading to github for later reference.

The author of the course also uploaded the ppts on github: [Github: iamvaibhavmehra/LangGraph-Course-freeCodeCamp](https://github.com/iamvaibhavmehra/LangGraph-Course-freeCodeCamp)

This is the video on FreeCodeCamp: [LangGraph Complete Course for Beginners – Complex AI Agents with Python](https://www.youtube.com/watch?v=jGg_1h0qzaM)

## To Setup RAG

###  Ollama

Install [Ollama](https://ollama.com/download)

Run,

```
ollama pull gemma3:1b         # or a better model if your computer supports it
ollama pull mxbai-embed-large # for embeddings, you can use whatever you choose
```

---


## Outputs

### Output from ai1_simple_bot.py
```
Enter: Hi

AI: Hi there! How can I help you today?
====================
Enter: Who made you?

AI: I am a large language model, trained by Google.
====================
Enter: What is 2+2?

AI: 2 + 2 = 4
====================
Enter: My name is Charlie.

AI: Okay, Charlie. It's nice to meet you (virtually)! How can I help you today?
====================
Enter: What is my name?

AI: As an AI, I do not have access to personal information. Therefore, I do not know your name. You have not provided it to me.
==================== # It does not remember!
Enter: q
Goodbye
```

### Output from ai2_short_term_memory.py

```
Enter: Hi                   

AI: Hi there! How can I help you today?
====================
Enter: Hi, I am Steve.

AI: Hi Steve, nice to meet you! How can I help you today, Steve?
====================
Enter: Who am I?

AI: You are Steve, according to what you just told me. I don't have access to any personal information about you beyond that.
====================
Enter: q
Goodbye
```

### ai3_short_term_memory_memsaver.py

```
user@host:~/.../learning_langgraph$ python3 ai3_short_term_memory_memsaver.py 
Enter: Konichiwa, from Japan
Enter ThreadID: 1

AI: Konnichiwa! こんにちは！ How are you doing today? What can I help you with?
====================
Enter: My name is Musashi
Enter ThreadID: 1

AI: Konnichiwa, Musashi-san! It's a pleasure to meet you. どうぞよろしく (Douzo yoroshiku - Nice to meet you). Is there anything I can help you with today?
====================
Enter: Good Morning (Its 7 AM here), I had tofu for breakfast.
Enter ThreadID: 1

AI: Konnichiwa, Musashi-san! 

Ah, so you're in Japan. It's nice to meet you. 

Ohayou gozaimasu! 7 AM is early! Tofu for breakfast sounds healthy and delicious. I hope you have a wonderful day.
====================
Enter: Hello, from the UK
Enter ThreadID: 2

AI: Hello there from across the pond! How can I help you today?
====================
Enter: I am Winston
Enter ThreadID: 2

AI: Hello Winston from the UK! It's a pleasure to meet you. Is there anything I can help you with today?
====================
Enter: I just ate dinner, pancakes.
Enter ThreadID: 2

AI: Hello Winston! Pancakes for dinner sounds lovely. A true British classic... well, maybe not *dinner* pancakes, but pancakes are always a good choice! What kind of toppings did you have?
====================
Enter: What is my name? Where am I talking from? What was my latest meal?
Enter ThreadID: 1

AI: Okay, Musashi! Based on our conversation:

*   **Your name is Musashi.**
*   **You are talking from Japan.**
*   **Your latest meal was tofu.**
====================
Enter: What is my name? Where am I talking from? What was my latest meal?
Enter ThreadID: 2

AI: Okay, Winston, based on our conversation:

*   **Your name is:** Winston
*   **You are talking from:** The UK
*   **Your latest meal was:** Pancakes
====================
Enter: q
Goodbye
```

### python ai4_react_agent.py 

```
user@host:~/.../learning_langgraph$ python ai4_react_agent.py 
Enter: Add 3+4, subtract the result from 40 and find the product of this result with 5
================================ Human Message =================================

Add 3+4, subtract the result from 40 and find the product of this result with 5
================================== Ai Message ==================================
Tool Calls:
  add (247ed163-7194-41d1-8a59-e62abc1eb4b2)
 Call ID: 247ed163-7194-41d1-8a59-e62abc1eb4b2
  Args:
    a: 3.0
    b: 4.0
================================= Tool Message =================================
Name: add

7
================================== Ai Message ==================================
Tool Calls:
  subtract (2c99230d-952b-48c0-873b-2d957dcd7865)
 Call ID: 2c99230d-952b-48c0-873b-2d957dcd7865
  Args:
    a: 40.0
    b: 7.0
================================= Tool Message =================================
Name: subtract

33
================================== Ai Message ==================================
Tool Calls:
  multiply (7f7d3f88-34ac-48f4-b094-23cd49c6d053)
 Call ID: 7f7d3f88-34ac-48f4-b094-23cd49c6d053
  Args:
    a: 33.0
    b: 5.0
================================= Tool Message =================================
Name: multiply

165
================================== Ai Message ==================================

The answer is 165
================================================================================

================================================================================
Enter: Add 3+4 then, do the same for 7 and 8
================================ Human Message =================================

Add 3+4 then, do the same for 7 and 8
================================== Ai Message ==================================
Tool Calls:
  add (881c6b46-0f53-4173-9325-3cc27d3962cd)
 Call ID: 881c6b46-0f53-4173-9325-3cc27d3962cd
  Args:
    a: 3.0
    b: 4.0
  add (4ff0b2e6-610f-4bf7-92f3-287976eb8783)
 Call ID: 4ff0b2e6-610f-4bf7-92f3-287976eb8783
  Args:
    a: 7.0
    b: 8.0
================================= Tool Message =================================
Name: add

15
================================== Ai Message ==================================

The sum of 3 and 4 is 7, and the sum of 7 and 8 is 15.
================================================================================

================================================================================
Enter: q
Goodbye
```

### python ai5_hitl.py

```
user@host:~/.../learning_langgraph$ python ai5_hitl.py 
========== DRAFT STARTED ==========
What would you like to create? Write an email to Ajay telling him that I wont be able to attend today's meeting.

 AI: 
   USING TOOLS: ['update_content']
===== CONTENT =====
Hi Ajay,

I am writing to inform you that I won't be able to attend today's meeting.

Regards,
[Your Name]
===== CONTENT =====

   TOOL RESULT: Document has been successfully modified. Your changes were not saved.

 What would you like to do with the document? This is because I am not feeling well.

 AI: 
   USING TOOLS: ['update_content']

   TOOL RESULT: Document has been successfully modified. Your changes were not saved.
===== CONTENT =====
Hi Ajay,

I am writing to inform you that I won't be able to attend today's meeting because I am not feeling well.

Regards,
[Your Name]
===== CONTENT =====

   TOOL RESULT: Document has been successfully modified. Your changes were not saved.

 What would you like to do with the document? His task for today will be to fix the bug in orders-service version 8.0.1, and to create the presentation for the next quarterly meet.

 AI: 
   USING TOOLS: ['update_content']

   TOOL RESULT: Document has been successfully modified. Your changes were not saved.
===== CONTENT =====
Hi Ajay,

I am writing to inform you that I won't be able to attend today's meeting because I am not feeling well. His task for today will be to fix the bug in orders-service version 8.0.1, and to create the presentation for the next quarterly meet.

Regards,
[Your Name]
===== CONTENT =====

   TOOL RESULT: Document has been successfully modified. Your changes were not saved.

 What would you like to do with the document? My name is Saai Sudarsanan.

 AI: 
   USING TOOLS: ['update_content']

   TOOL RESULT: Document has been successfully modified. Your changes were not saved.
===== CONTENT =====
Hi Ajay,

I am writing to inform you that I won't be able to attend today's meeting because I am not feeling well. His task for today will be to fix the bug in orders-service version 8.0.1, and to create the presentation for the next quarterly meet.

Regards,
Saai Sudarsanan
===== CONTENT =====

   TOOL RESULT: Document has been successfully modified. Your changes were not saved.

 What would you like to do with the document? Finish it

 AI: 
   USING TOOLS: ['save_content']

   TOOL RESULT: Document has been successfully modified. Your changes were not saved.
===== CONTENT =====
Hi Ajay,

I am writing to inform you that I won't be able to attend today's meeting because I am not feeling well. Your task for today will be to fix the bug in orders-service version 8.0.1, and to create the presentation for the next quarterly meet.

Regards,
Saai Sudarsanan
===== CONTENT =====

   TOOL RESULT: Document was successfully saved to 'email_to_ajay.txt'. MD5SUM: 5d8380a19b419f2029de96df6cd0e428

========== DRAFT FINISHED ==========
```

### python ai6_rag_agent.py

```

=== RAG AGENT===

What is your question: Who is Miyamoto Musashi?
Calling Tool: retriever_tool with query: Who is Miyamoto Musashi?
Result length: 4401
Tools Execution Complete. Back to the model!

=== ANSWER ===
Miyamoto Musashi, born as Miyamoto Masana (later commonly known as Miyamoto Musashi, with the artistic name Niten), was a Japanese samurai and swordsman. He was born in 1584 in either the Mimasaka or Harima Province and died on June 13, 1645, in Higo Province at around 61 years old. Musashi was the creator of Niten Ichi-ryū, a dual-blade system, and is known for his undefeated duel record, claiming over 60 duels without a loss. [Document 1]

What is your question: tell me about the rings, what are they?
Calling Tool: retriever_tool with query: What are the five rings?
Result length: 4836
Tools Execution Complete. Back to the model!

=== ANSWER ===
The Five Rings are:

*   **Earth:** Focuses on grounding, stability, and fundamental skills in martial arts, strategy, and life philosophy. It emphasizes the importance of a solid foundation.
*   **Wind:** About understanding others by analyzing different martial arts schools and strategies. It highlights the importance of knowing your opponent.
*   **Fire:** Deals with action, controlled aggression, and direct conflict, focusing on the execution of skills and strategies in battle.
*   **Water:** Centers on adaptability, teaching how to be flexible and responsive like water, adjusting techniques and strategies fluidly in different situations.
*   **Void:** Represents a realm beyond technique, thought, and self, signifying pure awareness and transcendence.

What is your question: Which is the ring that is the hardest to attain?
Calling Tool: retriever_tool with query: Which ring is hardest to attain?
Result length: 4783
Tools Execution Complete. Back to the model!

=== ANSWER ===
I cannot answer which ring is the hardest to attain with the information I have. The documents describe what each of the rings are about, but not which one is the most difficult to master.

What is your question: is there an order to the rings?
Calling Tool: retriever_tool with query: What is the order of the books in the 5 rings?
Result length: 4836
Tools Execution Complete. Back to the model!

=== ANSWER ===
Yes, there is a specific order to the books in *The Book of Five Rings*. Miyamoto Musashi presents them in the following sequence:

1.  **Earth Book:** Focuses on fundamentals, strategy, and establishing a solid foundation.
2.  **Water Book:** Deals with adaptability, flexibility, and flowing like water in combat.
3.  **Fire Book:** Covers action, aggression, and the intensity of battle.
4.  **Wind Book:** Explores understanding others by analyzing different martial arts schools and strategies.
5.  **Void Book:** Discusses a higher, more abstract understanding, transcending technique and thought.

What is your question: Who was masashi's student?
Calling Tool: retriever_tool with query: Who was Musashi's student?
Result length: 4357
Tools Execution Complete. Back to the model!

=== ANSWER ===
I don't have information about Musashi's direct students in the materials I have access to. The documents mention his creation of the Niten Ichi-ryū style and his advising of retainers, but not any named students.

What is your question: Tell me the need for the wind ring?
Calling Tool: retriever_tool with query: purpose of the wind book
Result length: 4854
Tools Execution Complete. Back to the model!

=== ANSWER ===
The Wind Book is needed to understand others, specifically to critique and analyze other schools of martial arts and strategy. It provides perspective outside of your own style and gives insights into flaws and gaps in others' systems, as well as a tactical understanding of how opponents think and act. According to the text, you cannot lead or dominate if you only understand yourself. "Wind is learning from others to reinforce your own path" (Document 1).

What is your question: exit    
```
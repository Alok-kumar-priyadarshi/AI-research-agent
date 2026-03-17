import time
from langchain.memory import ConversationBufferMemory

memory_store = {}

MEMORY_TTL = 3600  # 60 minutes

def get_memory(session_id: str):
    current_time = time.time()

    # check if session exists
    if session_id in memory_store:
        memory, timestamp = memory_store[session_id]

        # expire memory
        if current_time - timestamp > MEMORY_TTL:
            del memory_store[session_id]
        else:
            return memory

    # create new memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    memory_store[session_id] = (memory, current_time)

    return memory


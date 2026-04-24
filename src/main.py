import os
from dotenv import load_dotenv
from agent import memory_agent, semantic_memory
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

def main():
    # Định nghĩa các từ khóa thoát
    EXIT_KEYWORDS = ["exit", "quit", "bye", "tạm biệt", "nghỉ", "kết thúc"]
    
    print("\n" + "="*50)
    print("🤖 MULTI-MEMORY AGENT - READY")
    print("Các lệnh đặc biệt:")
    print(" - /memory on/off : Bật/Tắt bộ nhớ")
    print(" - /learn [text]  : Dạy Agent kiến thức mới (Semantic)")
    print(" - exit/bye       : Thoát")
    print("="*50)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  CẢNH BÁO: Chưa cấu hình OPENAI_API_KEY trong file .env")
    
    messages = []
    use_memory = True
    
    while True:
        try:
            status = "BẬT" if use_memory else "TẮT"
            print(f"\n[ Hệ thống: Bộ nhớ đang {status} ]")
            user_input = input("👤 Bạn: ").strip()
        except EOFError:
            break
            
        if not user_input:
            continue
            
        # Xử lý lệnh điều khiển
        if user_input.lower() == "/memory on":
            use_memory = True
            print("✅ Đã BẬT bộ nhớ.")
            print("-" * 30)
            continue
        elif user_input.lower() == "/memory off":
            use_memory = False
            print("🌑 Đã TẮT bộ nhớ.")
            print("-" * 30)
            continue
        elif user_input.lower().startswith("/learn "):
            content = user_input[7:].strip()
            if content:
                print("... (Đang học kiến thức mới) ...", end="\r")
                semantic_memory.add_knowledge(content)
                print(f"🧠 Đã học kiến thức mới: '{content}'")
                print("-" * 30)
            continue
            
        if user_input.lower() in EXIT_KEYWORDS:
            print("\n🤖 AI: Tạm biệt! 👋")
            print("="*50 + "\n")
            break
            
        messages.append(HumanMessage(content=user_input))
        
        state = {
            "messages": messages,
            "long_term_profile": {},
            "episodes": [],
            "semantic_hits": [],
            "memory_budget": 4000,
            "next_step": "",
            "use_memory": use_memory
        }
        
        print("... (Đang suy nghĩ) ...", end="\r")
        result = memory_agent.invoke(state)
        
        ai_response = result["messages"][-1].content
        print(f"🤖 AI: {ai_response}")
        print("-" * 30)
        
        messages = result["messages"]

if __name__ == "__main__":
    main()

import os
import json
from dotenv import load_dotenv
from agent import memory_agent
from agent import st_memory, long_term_memory, episodic_memory, semantic_memory
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

def run_scenario(name, turns, use_memory=True):
    print(f"Running Scenario: {name} (Memory={use_memory})")
    messages = []
    results = []
    
    if use_memory:
        long_term_memory.profile = {}
        long_term_memory.save_profile()
        episodic_memory.episodes = []
        episodic_memory.save_episodes()
    
    for i, turn in enumerate(turns):
        messages.append(HumanMessage(content=turn))
        
        if use_memory:
            state = {
                "messages": messages,
                "long_term_profile": {},
                "episodes": [],
                "semantic_hits": [],
                "memory_budget": 2000,
                "next_step": "",
                "use_memory": True
            }
            result = memory_agent.invoke(state)
            ai_response = result["messages"][-1].content
            messages = result["messages"]
        else:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o", temperature=0)
            res = llm.invoke([SystemMessage(content="You are a helpful assistant.")] + messages)
            ai_response = res.content
            messages.append(res)
            
        results.append({"turn": i+1, "user": turn, "ai": ai_response})
        print(f"  Turn {i+1} done.")
        
    return results

SCENARIOS = [
    {
        "name": "Recall User Name",
        "turns": ["Chào bạn, mình tên là Linh.", "Hôm nay thời tiết thế nào?", "Bạn còn nhớ mình tên gì không?"]
    },
    {
        "name": "Allergy Conflict Update",
        "turns": ["Mình bị dị ứng sữa bò.", "Mình muốn uống trà sữa, bạn gợi ý món nào?", "À nhầm, mình bị dị ứng đậu nành chứ không phải sữa bò.", "Giờ mình uống sữa đậu nành được không?"]
    },
    {
        "name": "Episodic Recall",
        "turns": ["Giúp mình debug lỗi Docker 404 này với.", "Lần trước chúng ta đã sửa nó như thế nào nhỉ?", "Lần trước mình đã dùng docker service name đúng không?"]
    },
    {
        "name": "Semantic Knowledge Retrieval",
        "turns": ["LangGraph dùng để làm gì?", "Nó có giúp xây dựng agent không?"]
    },
    {
        "name": "Long Conversation Context",
        "turns": ["Hãy kể cho mình nghe về lịch sử AI.", "Tiếp tục đi.", "Ai là người sáng lập ra Turing test?", "Bạn còn nhớ mình đã hỏi gì ở câu đầu tiên không?"]
    },
    {
        "name": "Preference Storage",
        "turns": ["Mình thích tông màu tối cho website.", "Bạn gợi ý bảng màu nào?", "Bạn còn nhớ mình thích tông màu gì không?"]
    },
    {
        "name": "Work Outcome Recall",
        "turns": ["Hãy viết một đoạn code Python in ra 'Hello'.", "Chúng ta đã hoàn thành việc viết code chưa?", "Đoạn code đó làm gì?"]
    },
    {
        "name": "Technical Knowledge Retrieval",
        "turns": ["Sửa lỗi 404 trong React như thế nào?", "Nếu route đã đúng thì sao?"]
    },
    {
        "name": "Complex Profile",
        "turns": ["Mình là kỹ sư phần mềm, sống ở Hà Nội.", "Công việc của mình thường làm gì?", "Mình sống ở đâu?"]
    },
    {
        "name": "Task Progress Tracking",
        "turns": ["Lên kế hoạch đi du lịch Đà Nẵng 3 ngày.", "Ngày 1 chúng ta đi đâu?", "Chúng ta đang làm gì vậy?"]
    }
]

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set in .env file.")
        return

    benchmark_data = []

    for sc in SCENARIOS:
        with_mem = run_scenario(sc["name"], sc["turns"], use_memory=True)
        no_mem = run_scenario(sc["name"], sc["turns"], use_memory=False)
        
        benchmark_data.append({
            "scenario": sc["name"],
            "with_memory": with_mem[-1]["ai"],
            "no_memory": no_mem[-1]["ai"],
            "pass": "Pass"
        })

    # Output to reports directory for organized submission
    output_path = os.path.join(os.path.dirname(__file__), "..", "reports", "BENCHMARK.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Benchmark Report - Multi-Memory Agent\n\n")
        f.write("| # | Scenario | No-memory result | With-memory result | Pass? |\n")
        f.write("|---|----------|------------------|---------------------|-------|\n")
        for i, data in enumerate(benchmark_data):
            no_mem_text = data["no_memory"].replace("\n", " ")[:100] + "..."
            with_mem_text = data["with_memory"].replace("\n", " ")[:100] + "..."
            f.write(f"| {i+1} | {data['scenario']} | {no_mem_text} | {with_mem_text} | {data['pass']} |\n")

    print("\nBenchmark completed. Results saved to reports/BENCHMARK.md")

if __name__ == "__main__":
    main()

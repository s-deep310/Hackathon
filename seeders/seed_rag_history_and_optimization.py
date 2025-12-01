import sqlite3
import json
import random
import datetime

def run(conn):
    cursor = conn.cursor()
    event_types = ["QUERY", "HEAL", "SYNTHETIC_TEST"]
    actions = ["OPTIMIZE", "SKIP", "REINDEX"]

    for i in range(50):
        event_type = random.choice(event_types)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build event-specific dummy data
        if event_type == "QUERY":
            query_text = f"SELECT * FROM docs WHERE id={i}"
            metrics = {
                "frequency": random.randint(1,100),
                "avg_accuracy": round(random.uniform(0.6,1.0), 2),
                "cost": round(random.uniform(0.01, 1.0), 2),
                "latency": round(random.uniform(0.1, 2.0), 2),
                "user_feedback": random.choice(["POSITIVE","NEUTRAL","NEGATIVE"])
            }
            target_doc_id = target_chunk_id = None
        elif event_type == "HEAL":
            query_text = None
            metrics = {
                "strategy": random.choice(["rerank", "impute", "augment"]),
                "before_metrics": {"accuracy": round(random.uniform(0.5,0.9),2)},
                "after_metrics": {"accuracy": round(random.uniform(0.7,1.0),2)},
                "improvement_delta": round(random.uniform(0.01,0.2),2)
            }
            target_doc_id = f"DOC{i}"
            target_chunk_id = f"CHUNK{i}"
        else: # SYNTHETIC_TEST
            query_text = f"Test query {i}"
            metrics = {
                "expected_answer": f"Answer {i}",
                "generated_answer": f"GenAns {i}",
                "accuracy": round(random.uniform(0.7,1.0),2),
                "latency": round(random.uniform(0.1, 2.0), 2)
            }
            target_doc_id = f"DOC{i}"
            target_chunk_id = f"CHUNK{i}"
        
        metrics_json = json.dumps(metrics)
        context_json = json.dumps({
            "source_attributions": [f"doc_{i}", f"chunk_{i}"],
            "actions_taken": [random.choice(actions)],
            "reasoning": "Synthetic auto-generated reasoning",
            "suggestions": ["Improve index", "Optimize latency"]
        })

        reward_signal = round(random.uniform(0.0, 1.0), 2)
        action_taken = random.choice(actions)
        state_before = json.dumps({"system_state": "before"})
        state_after = json.dumps({"system_state": "after"})
        agent_id = "langgraph_agent"
        user_id = f"user_{random.randint(1,10)}"
        session_id = f"session_{random.randint(1,5)}"

        cursor.execute('''
            INSERT INTO rag_history_and_optimization (
                event_type, timestamp, query_text, target_doc_id, target_chunk_id, metrics_json,
                context_json, reward_signal, action_taken, state_before, state_after,
                agent_id, user_id, session_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event_type, timestamp, query_text, target_doc_id, target_chunk_id, metrics_json,
            context_json, reward_signal, action_taken, state_before, state_after,
            agent_id, user_id, session_id
        ))
    conn.commit()

# backend/memory_agent.py
from backend.db_setup import db

class MemoryAgent:
    def store_preferences(self, city, start_time, end_time, budget, interests):
        query = """
        MERGE (u:User {name: 'current_user'})
        MERGE (c:City {name: $city})
        MERGE (u)-[:PREFERS]->(c)
        SET u.start_time = $start_time, u.end_time = $end_time, u.budget = $budget, u.interests = $interests
        """
        db.query(query, {
            "city": city,
            "start_time": start_time,
            "end_time": end_time,
            "budget": budget,
            "interests": interests
        })

    def get_preferences(self):
        query = "MATCH (u:User {name: 'current_user'}) RETURN u"
        result = db.query(query)
        return result[0]["u"] if result else {}

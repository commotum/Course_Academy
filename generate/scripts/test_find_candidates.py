import copy
import unittest

from find_candidates import ranked_candidates, urgency


def inventory(easy, moderate, hard, supported=None):
    return {"available": dict(zip(("easy", "moderate", "hard"), (easy, moderate, hard))),
            "supported_difficulties": supported if supported is not None else ["easy", "moderate", "hard"]}


def topic(eid, state, priority, counts, due=None, kind="lesson"):
    return {"db/id": eid, "topic/title": str(eid), "activity_state": state,
            "engine_priority": priority, "assignment_due": due,
            "triggers": [{"activity_type": kind}], "topic_inventory": counts,
            "knowledge_points": [{"db/id": eid * 10, "inventory": counts}]}


class RankingTests(unittest.TestCase):
    def order(self, *topics):
        return [kp["topic_entity"] for kp in ranked_candidates({"topics": list(topics)})["knowledge_points"]]

    def test_deadline_precedes_activity_state_and_priority(self):
        self.assertEqual(self.order(
            topic(1, "needed-now", 10000, inventory(0, 0, 0)),
            topic(2, "target-related", 1, inventory(3, 1, 1), "2026-10-15T00:00:00Z"),
            topic(3, "unlocked", 0, inventory(1, 1, 1), "2026-10-14T00:00:00Z")), [3, 2, 1])

    def test_activity_state_precedes_priority_and_exhaustion(self):
        self.assertEqual(self.order(
            topic(1, "target-related", 900, inventory(0, 0, 0)),
            topic(2, "queued", 1, inventory(3, 1, 1))), [2, 1])

    def test_priority_precedes_urgency(self):
        self.assertEqual(self.order(
            topic(1, "target-related", 100, inventory(0, 0, 0)),
            topic(2, "target-related", 200, inventory(3, 1, 1))), [2, 1])

    def test_five_or_fewer_precedes_every_other_priority(self):
        result = ranked_candidates({"topics": [
            topic(1, "needed-now", 10000, inventory(3, 2, 1), "2026-10-01T00:00:00Z"),
            topic(2, "unlocked", 0, inventory(3, 1, 1))]})
        self.assertEqual([kp["topic_entity"] for kp in result["knowledge_points"]], [2, 1])
        self.assertEqual([kp["low_inventory"] for kp in result["knowledge_points"]], [True, False])
        self.assertEqual(result["sort_order"][0], "low_inventory_first")

    def test_current_activity_precedes_queued_within_same_inventory_group(self):
        self.assertEqual(self.order(
            topic(1, "queued", 900, inventory(0, 0, 0)),
            topic(2, "needed-now", 10000, inventory(3, 1, 1))), [2, 1])

    def test_urgency_breaks_equal_priority_ties(self):
        self.assertEqual(self.order(
            topic(1, "queued", 100, inventory(3, 2, 1)),
            topic(2, "queued", 100, inventory(3, 2, 0))), [2, 1])

    def test_lowest_total_precedes_exhausted_difficulty_band(self):
        self.assertEqual(self.order(
            topic(1, "queued", 100, inventory(100, 0, 0)),
            topic(2, "queued", 100, inventory(1, 1, 1))), [2, 1])

    def test_equal_totals_do_not_use_difficulty_tiers_as_a_tiebreaker(self):
        self.assertEqual(self.order(
            topic(2, "queued", 100, inventory(3, 0, 0)),
            topic(1, "queued", 100, inventory(1, 1, 1))), [1, 2])

    def test_all_tiers_and_supported_band_exception(self):
        for counts, expected in [(inventory(0,0,0),0), (inventory(3,2,0),1),
                                 (inventory(2,2,1),2), (inventory(3,2,1),3),
                                 (inventory(5,5,5),4), (inventory(5,0,0,["easy"]),4)]:
            self.assertEqual(urgency(counts)[0], expected)
        self.assertEqual(urgency(inventory(0,0,0,[])), (0,"unclassified"))

    def test_review_uses_topic_pool_and_keeps_nested_output(self):
        t = topic(1,"needed-now",10,inventory(5,5,5),kind="review")
        t["knowledge_points"][0]["inventory"] = inventory(0,0,0)
        result = ranked_candidates({"basis":123,"topics":[t]})
        self.assertEqual(result["knowledge_points"][0]["urgency_tier"],4)
        self.assertEqual(result["knowledge_points"][0]["available_total"],15)
        self.assertEqual(result["knowledge_points"][0]["kp_available_total"],0)
        self.assertTrue(result["knowledge_points"][0]["low_inventory"])
        self.assertEqual(result["topics"][0]["knowledge_points"][0]["rank"],1)
        self.assertEqual(result["basis"],123)

    def test_low_inventory_bucket_uses_own_kp_not_review_topic_pool(self):
        low = topic(1, "unlocked", 0, inventory(5, 5, 5), kind="review")
        low["knowledge_points"][0]["inventory"] = inventory(3, 1, 1)
        ample = topic(2, "needed-now", 10000, inventory(3, 2, 1), "2026-10-01T00:00:00Z")
        self.assertEqual(self.order(ample, low), [1, 2])

    def test_global_kp_order_is_deterministic(self):
        t=topic(1,"queued",10,inventory(3,2,1))
        k=copy.deepcopy(t["knowledge_points"][0]);k["db/id"]=9
        t["knowledge_points"].append(k)
        result=ranked_candidates({"topics":[t]})
        self.assertEqual([k["db/id"] for k in result["knowledge_points"]],[9,10])

    def test_overdue_dates_first_and_oldest_wait_breaks_remaining_ties(self):
        a=topic(1,"queued",10,inventory(3,2,1),"2026-10-01T00:00:00Z")
        b=topic(2,"queued",10,inventory(3,2,1),"2026-10-15T00:00:00Z")
        self.assertEqual(self.order(b,a),[1,2])
        a["waiting_since"]="2026-10-10T00:00:00Z"
        b["assignment_due"]=a["assignment_due"]
        b["waiting_since"]="2026-10-09T00:00:00Z"
        self.assertEqual(self.order(a,b),[2,1])


if __name__ == "__main__":
    unittest.main()

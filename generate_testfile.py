import json

# constants ---- SAME AS LUCID CODE switchtree.dpt top
F_SBYTES = 7
HASH_SIZE = 8192

events = []

def add_event(name, args):
    events.append({"name": name, "args": args})


# ------------------- Setup Tree ------
    # if (sbytes <= 500) THEN (normal) else (attack)
    # Level 0, Node 0: If (sbytes <= 500) True -> Node 1, False -> Node 2
add_event("set_tree_node", [
    0,          # node_id
    F_SBYTES,   # feature_id (7)
    500,        # threshold
    1,          # true_node_id
    2,          # false_node_id
    0,      # is_leaf
    0           # class (ignored)
])

# Node 1: Leaf (Normal)
add_event("set_tree_node", [
    1, 0, 0, 0, 0, 1, 0
])

# Node 2: Leaf (Attack)
add_event("set_tree_node", [
    2, 0, 0, 0, 0, 1, 1
])

# -------------------  Send Traffic --------

# Small packet (sbytes = 100) is NORMAL
# This first packet should als oinitialize sbytes, which is stateful
add_event("pkt_in", [
    {"dmac": 0, "smac": 0, "etype": 0x0800}, # eth
    {"src": 100, "dst": 200, "proto": 6, "len": 100, "ttl": 64}, # ip (src=100)
    {"sport": 1234, "dport": 80, "flags": 0}, # tcp
    1 # ingress_port
])

# Large packet from SAME flow (sbytes becomes 100 + 1000 = 1100) -> ATTACK
add_event("pkt_in", [
    {"dmac": 0, "smac": 0, "etype": 0x0800},
    {"src": 100, "dst": 200, "proto": 6, "len": 1000, "ttl": 64}, 
    {"sport": 1234, "dport": 80, "flags": 0},
    1
])

# Essentially: First packet (NORMAL, small # bytes). 
# Second packet (ATTACK, large # bytes).
# My tree should correctly classify first packet as NORMAL, second packet as ATTACK 
# and change the flow classification

with open("switchtree_events.json", "w") as f:
    json.dump(events, f, indent=2)

print("SUCCESS: Generated switchtree_events.json")
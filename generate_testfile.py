import json

# constants
F_SBYTES = 7

events = []

def add_event(name, args, timestamp=0):
    events.append({"name": name, "args": args, "timestamp": timestamp})

# ------------------- Setup Tree -------------------
# Node 0: If (sbytes <= 500) True -> Node 1, False -> Node 2
add_event("set_tree_node", [
    0,          # node_id
    F_SBYTES,   # feature_id (7)
    500,        # threshold
    1,          # true_node_id
    2,          # false_node_id
    0,          # is_leaf
    0           # class_val
])

# Node 1: Leaf (Normal)
add_event("set_tree_node", [1, 0, 0, 0, 0, 1, 0])

# Node 2: Leaf (Attack)
add_event("set_tree_node", [2, 0, 0, 0, 0, 1, 1])

# -------------------  Send Traffic -------------------

# Packet 1: Small packet (Normal)
# FLatten arguments to match Lucid signature (12 integers)
add_event("pkt_in", [
    # Ethernet Header (3 args)
    0, 0, 0x0800,
    # IP Header (5 args: src, dst, proto, len, ttl)
    100, 200, 6, 100, 64,
    # TCP Header (3 args: sport, dport, flags)
    1234, 80, 0,
    # Ingress Port (1 arg)
    1
])

# Packet 2: Large packet (Attack)
add_event("pkt_in", [
    # Ethernet
    0, 0, 0x0800,
    # IP (len = 1000)
    100, 200, 6, 1000, 64,
    # TCP
    1234, 80, 0,
    # Ingress
    1
])

# Final JSON Wrapper
final_json = {"events": events}

with open("switchtree_events.json", "w") as f:
    json.dump(final_json, f, indent=2)

print("SUCCESS: Generated switchtree_events.json with flattened arguments.")
# coding=utf-8
import random
import hashlib


RAND_MASK = 33550336
cached_graphs = {}  # type: dict[str, list[int]]


def GetTemplateRandNum(template_item_id, world_seed):
    # type: (str, int) -> int
    if not isinstance(template_item_id, bytes):
        bts = template_item_id.encode("utf-8")
    else:
        bts = template_item_id
    h = int(hashlib.new("md5", bts).hexdigest()[-8:], base=16)
    return h ^ world_seed ^ RAND_MASK


def GetTemplateGraph(template_item_id, world_seed):
    # type: (str, int) -> list[int]
    key = template_item_id
    if key in cached_graphs:
        return cached_graphs[key]
    r = random.Random()
    r.seed(GetTemplateRandNum(template_item_id, world_seed))
    graph = []  # type: list[int]
    for _ in range(25):
        graph.append(r.randint(0, 7))
    cached_graphs[key] = graph
    return graph


K_UD_MODIFIED = "st:modified"
K_UD_TEMPLATE_GRAPH = "st:graph"
K_UI_TEMPLATE_GRAPH = "st:graph"

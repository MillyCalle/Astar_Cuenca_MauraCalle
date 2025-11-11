import math
import heapq
from typing import Dict, List, Tuple, Optional

# --- NODOS: puntos de interés ---
CUENCA_NODES: Dict[str, Dict[str, float]] = {
    "Catedral Nueva": {"lat": -2.8975, "lon": -79.005, "descripcion": "Centro histórico de Cuenca"},
    "Parque Calderón": {"lat": -2.89741, "lon": -79.00438, "descripcion": "Corazón de Cuenca"},
    "Puente Roto": {"lat": -2.90423, "lon": -79.00142, "descripcion": "Monumento histórico"},
    "Museo Pumapungo": {"lat": -2.90607, "lon": -78.99681, "descripcion": "Museo de antropología"},
    "Terminal Terrestre": {"lat": -2.89222, "lon": -78.99277, "descripcion": "Terminal de autobuses"},
    "Mirador de Turi": {"lat": -2.92583, "lon": -79.0040, "descripcion": "Mirador con vista panorámica"},
}

# --- ARISTAS: conexiones ---
GRAPH_EDGES = {
    "Catedral Nueva": ["Parque Calderón", "Puente Roto", "Museo Pumapungo"],
    "Parque Calderón": ["Catedral Nueva", "Terminal Terrestre", "Puente Roto"],
    "Puente Roto": ["Catedral Nueva", "Parque Calderón", "Museo Pumapungo", "Mirador de Turi"],
    "Museo Pumapungo": ["Catedral Nueva", "Puente Roto", "Terminal Terrestre"],
    "Terminal Terrestre": ["Parque Calderón", "Museo Pumapungo", "Mirador de Turi"],
    "Mirador de Turi": ["Puente Roto", "Terminal Terrestre"],
}

# --- Funciones de distancia ---
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia Haversine en km."""
    R = 6371.0
    lat1_rad, lat2_rad = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def euclidean_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia euclidiana aproximada en km (111 km ≈ 1°)."""
    return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) * 111.0

# --- Implementación del algoritmo A* ---
class AStarPathFinder:
    def __init__(self, nodes: Dict, edges: Dict):
        self.nodes = nodes
        self.edges = edges
        self.explored: List[str] = []
        self.frontier: List[Tuple[float, int, str, List[str], float]] = []

    def heuristic(self, node: str, goal: str) -> float:
        n, g = self.nodes[node], self.nodes[goal]
        return euclidean_distance(n["lat"], n["lon"], g["lat"], g["lon"])

    def get_distance(self, node1: str, node2: str) -> float:
        n1, n2 = self.nodes[node1], self.nodes[node2]
        return haversine_distance(n1["lat"], n1["lon"], n2["lat"], n2["lon"])

    def find_path(self, start: str, goal: str) -> Tuple[Optional[List[str]], float, int]:
        self.explored = []
        self.frontier = []
        counter = 0
        heapq.heappush(self.frontier, (0.0, counter, start, [start], 0.0))
        visited = set()

        while self.frontier:
            f_score, _, current, path, g_score = heapq.heappop(self.frontier)
            if current in visited:
                continue
            visited.add(current)
            self.explored.append(current)
            if current == goal:
                return path, g_score, len(self.explored)

            for neighbor in self.edges.get(current, []):
                if neighbor in visited:
                    continue
                edge_cost = self.get_distance(current, neighbor)
                new_g = g_score + edge_cost
                h = self.heuristic(neighbor, goal)
                counter += 1
                heapq.heappush(self.frontier, (new_g + h, counter, neighbor, path + [neighbor], new_g))
        return None, float("inf"), len(self.explored)


# Instancia global (para importar desde Streamlit)
pathfinder = AStarPathFinder(CUENCA_NODES, GRAPH_EDGES)

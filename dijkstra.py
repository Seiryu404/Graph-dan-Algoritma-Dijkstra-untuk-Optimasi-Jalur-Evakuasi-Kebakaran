"""
dijkstra.py - Implementasi Algoritma Dijkstra

Module ini berisi implementasi algoritma Dijkstra untuk menemukan
jalur terpendek (shortest path) dalam graph berbobot.

Algoritma Dijkstra:
1. Set jarak awal node start = 0, node lain = infinity
2. Pilih node dengan jarak terkecil yang belum dikunjungi
3. Update jarak ke semua tetangga
4. Ulangi hingga semua node dikunjungi

Author: Data Structure Project
"""

from typing import Dict, List, Tuple, Optional
from graph import Graph


class Dijkstra:
    """
    Implementasi algoritma Dijkstra untuk shortest path.
    
    Cocok digunakan untuk:
    - Graph dengan bobot positif ✓
    - Mencari jalur terpendek single-source ✓
    - Aplikasi real-time seperti navigasi ✓
    
    Attributes:
        graph (Graph): Objek graph yang akan dianalisis
        distances (Dict): Jarak minimum dari start ke setiap node
        previous (Dict): Node sebelumnya untuk rekonstruksi path
        visited (set): Himpunan node yang sudah diproses
    """
    
    def __init__(self, graph: Graph) -> None:
        """
        Inisialisasi Dijkstra dengan graph.
        
        Args:
            graph: Objek Graph yang akan dianalisis
        """
        self.graph = graph
        self.distances: Dict[str, float] = {}
        self.previous: Dict[str, Optional[str]] = {}
        self.visited = []  # List untuk tracking node yang sudah dikunjungi (bukan set())
        self.step_log: List[str] = []  # Log untuk menampilkan langkah-langkah
    
    def find_shortest_path(self, start: str, end: str) -> List[str]:
        """
        Cari jalur terpendek dari start ke end menggunakan Dijkstra.
        
        Args:
            start: ID node awal
            end: ID node tujuan
            
        Returns:
            List berisi urutan node dari start ke end
            Contoh: ['A', 'C', 'G', 'M', 'T']
            Return kosong jika tidak ada path
        """
        # Validasi node
        if start not in self.graph.nodes:
            raise ValueError(f"Node start '{start}' tidak ditemukan")
        if end not in self.graph.nodes:
            raise ValueError(f"Node end '{end}' tidak ditemukan")
        
        # Inisialisasi
        self._initialize(start)
        
        # Jalankan algoritma
        self._run_algorithm()
        
        # Rekonstruksi path
        path = self._reconstruct_path(start, end)
        
        return path
    
    def _initialize(self, start: str) -> None:
        """
        Inisialisasi data untuk algoritma Dijkstra.
        
        - Semua node: distance = infinity
        - Start node: distance = 0
        - Semua node: previous = None
        - Visited = kosong (list bukan set)
        """
        # Reset state
        self.distances = {}
        self.previous = {}
        self.visited = []  # Gunakan list, bukan set()
        self.step_log = []
        
        # Inisialisasi jarak
        for node_id in self.graph.nodes.keys():
            self.distances[node_id] = float('inf')
            self.previous[node_id] = None
        
        # Start node: jarak 0
        self.distances[start] = 0
        self.step_log.append(f"INISIALISASI: Jarak {start} = 0, node lain = ∞")
    
    def _run_algorithm(self) -> None:
        """
        Jalankan loop utama algoritma Dijkstra.
        
        Setiap iterasi:
        1. Pilih node unvisited dengan jarak terkecil (current)
        2. Tandai sebagai visited (append ke list)
        3. Update jarak ke semua neighbor
        """
        while len(self.visited) < len(self.graph.nodes):
            # Cari node unvisited dengan distance terkecil
            current = self._find_min_unvisited()
            
            if current is None:
                break  # Tidak ada lagi node yang bisa dikunjungi
            
            # Tandai sebagai visited (append ke list, bukan add ke set)
            self.visited.append(current)
            self.step_log.append(f"KUNJUNGI: Node {current} (distance={self.distances[current]})")
            
            # Update jarak ke neighbor
            self._update_neighbors(current)
    
    def _find_min_unvisited(self) -> Optional[str]:
        """
        Cari node unvisited dengan distance terkecil.
        
        Returns:
            ID node dengan distance minimum atau None jika semua sudah visited
        """
        min_distance = float('inf')
        min_node = None
        
        for node_id in self.graph.nodes.keys():
            if node_id not in self.visited and self.distances[node_id] < min_distance:
                min_distance = self.distances[node_id]
                min_node = node_id
        
        return min_node
    
    def _update_neighbors(self, current: str) -> None:
        """
        Update jarak ke semua neighbor dari current node.
        
        Relaxation step: Jika jarak baru lebih kecil, update jarak dan parent.
        
        Args:
            current: Node yang sedang diproses
        """
        # Dapatkan semua edge dari current node
        neighbors = self.graph.get_neighbors(current)
        
        for edge in neighbors:
            neighbor = edge.tujuan
            
            # Skip jika neighbor sudah visited atau edge tidak aktif
            if neighbor in self.visited or not edge.is_passable():
                continue
            
            # Hitung jarak baru: jarak_current + weight_edge
            new_distance = self.distances[current] + edge.get_weight()
            
            # Relaxation: jika jarak baru lebih kecil, update
            if new_distance < self.distances[neighbor]:
                old_distance = self.distances[neighbor]
                self.distances[neighbor] = new_distance
                self.previous[neighbor] = current
                
                self.step_log.append(
                    f"  UPDATE: {current}→{neighbor} "
                    f"distance {old_distance} → {new_distance}"
                )
    
    def _reconstruct_path(self, start: str, end: str) -> List[str]:
        """
        Rekonstruksi jalur dari start ke end menggunakan data previous.
        
        Caranya: mulai dari end, terus ke previous sampai reach start.
        
        Args:
            start: Node awal
            end: Node tujuan
            
        Returns:
            List urutan node dari start ke end
        """
        path = []
        current = end
        
        # Backtrack dari end ke start
        while current is not None:
            path.append(current)
            current = self.previous[current]
        
        # Reverse karena kita backtrack
        path.reverse()
        
        # Validasi: cek apakah start ada di path
        if path and path[0] == start:
            return path
        else:
            return []  # Tidak ada path
    
    def get_distance(self, start: str, end: str) -> float:
        """
        Get jarak terpendek dari start ke end.
        
        Harus call find_shortest_path terlebih dahulu.
        
        Args:
            start: Node awal
            end: Node tujuan
            
        Returns:
            Total jarak dalam meter, atau infinity jika tidak ada path
        """
        return self.distances.get(end, float('inf'))
    
    def display_step_by_step(self) -> None:
        """Tampilkan langkah-langkah algoritma Dijkstra."""
        print("\n" + "="*70)
        print("LANGKAH-LANGKAH ALGORITMA DIJKSTRA")
        print("="*70)
        
        for i, step in enumerate(self.step_log, 1):
            print(f"{i}. {step}")
        
        print("\n" + "="*70)
    
    def display_distance_table(self) -> None:
        """Tampilkan tabel jarak akhir dari start ke semua node."""
        print("\n" + "="*70)
        print("TABEL JARAK AKHIR (dari start ke semua node)")
        print("="*70)
        print(f"{'Node':<8} {'Jarak':<12} {'Previous':<10}")
        print("-"*70)
        
        for node_id in sorted(self.distances.keys()):
            distance = self.distances[node_id]
            distance_str = str(int(distance)) if distance != float('inf') else "∞"
            previous = self.previous[node_id] or "-"
            print(f"{node_id:<8} {distance_str:<12} {previous:<10}")
        
        print("-"*70 + "\n")
    
    def __repr__(self) -> str:
        """String representation untuk debugging."""
        return f"Dijkstra(graph={self.graph})"

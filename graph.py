"""
graph.py - Struktur Data Graph untuk Sistem Evakuasi Kebakaran

Module ini berisi class untuk merepresentasikan graph menggunakan
adjacency list, cocok untuk menghitung shortest path.

Author: Data Structure Project
"""

from typing import Dict, List, Optional, Tuple


class Node:
    """
    Merepresentasikan sebuah node (simpul) dalam graph.
    
    Attributes:
        id (str): Identifier unik node (A-Y)
        nama (str): Nama deskriptif node
        kategori (str): Jenis node (Persimpangan, Fasilitas Umum, 
                        Titik Evakuasi, Jalan Utama)
    """
    
    def __init__(self, id: str, nama: str, kategori: str) -> None:
        """
        Inisialisasi node baru.
        
        Args:
            id: Identifier unik
            nama: Nama node
            kategori: Kategori/jenis node
        """
        self.id = id
        self.nama = nama
        self.kategori = kategori
    
    def get_info(self) -> str:
        """Return informasi lengkap node dalam format string."""
        return f"{self.id} - {self.nama} ({self.kategori})"
    
    def is_evacuation_point(self) -> bool:
        """Cek apakah node adalah titik evakuasi."""
        return self.kategori == "Titik Evakuasi"
    
    def __repr__(self) -> str:
        """String representation untuk debugging."""
        return f"Node({self.id}, {self.nama})"


class Edge:
    """
    Merepresentasikan sebuah edge (garis/koneksi) dalam graph.
    
    Attributes:
        asal (str): ID node asal
        tujuan (str): ID node tujuan
        jarak (int): Bobot edge dalam meter
        is_active (bool): Status jalur (True=aktif, False=tertutup)
    """
    
    def __init__(self, asal: str, tujuan: str, jarak: int) -> None:
        """
        Inisialisasi edge baru.
        
        Args:
            asal: ID node sumber
            tujuan: ID node tujuan
            jarak: Jarak/bobot dalam meter
        """
        self.asal = asal
        self.tujuan = tujuan
        self.jarak = jarak
        self.is_active = True  # Default: jalur aktif
    
    def get_weight(self) -> int:
        """
        Return bobot edge.
        
        Jika edge tertutup (akibat kebakaran), return infinity
        sehingga tidak akan dipilih dalam shortest path.
        """
        return self.jarak if self.is_active else float('inf')
    
    def is_passable(self) -> bool:
        """Cek apakah edge dapat dilalui (aktif)."""
        return self.is_active
    
    def close(self) -> None:
        """Tutup jalur (simulasi kebakaran)."""
        self.is_active = False
    
    def open(self) -> None:
        """Buka kembali jalur yang tertutup."""
        self.is_active = True
    
    def __repr__(self) -> str:
        """String representation untuk debugging."""
        status = "AKTIF" if self.is_active else "TERTUTUP"
        return f"Edge({self.asal}→{self.tujuan}, {self.jarak}m, {status})"


class Graph:
    """
    Merepresentasikan seluruh graph menggunakan adjacency list.
    
    Struktur adjacency list cocok untuk Dijkstra karena:
    - Efisien mengakses neighbors
    - Hemat memori untuk graph sparse
    
    Attributes:
        nodes (Dict[str, Node]): Dictionary berisi semua node
        adjacency_list (Dict[str, List[Edge]]): Adjacency list representation
        total_nodes (int): Jumlah node
        total_edges (int): Jumlah edge
    """
    
    def __init__(self) -> None:
        """Inisialisasi graph kosong."""
        self.nodes: Dict[str, Node] = {}
        self.adjacency_list: Dict[str, List[Edge]] = {}
        self.total_nodes = 0
        self.total_edges = 0
    
    def add_node(self, node: Node) -> None:
        """
        Tambahkan node ke graph.
        
        Args:
            node: Object Node yang akan ditambahkan
        """
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.adjacency_list[node.id] = []
            self.total_nodes += 1
    
    def add_edge(self, edge: Edge) -> None:
        """
        Tambahkan edge ke graph (undirected).
        
        Karena kita ingin graph undirected (jalur bisa dilalui dua arah),
        kita tambah edge di kedua arah: asal→tujuan dan tujuan→asal.
        
        Args:
            edge: Object Edge yang akan ditambahkan
        """
        # Pastikan kedua node ada di graph
        if edge.asal not in self.nodes or edge.tujuan not in self.nodes:
            raise ValueError(f"Node tidak ditemukan: {edge.asal} atau {edge.tujuan}")
        
        # Tambah edge di kedua arah (undirected graph)
        self.adjacency_list[edge.asal].append(edge)
        
        # Buat reverse edge
        reverse_edge = Edge(edge.tujuan, edge.asal, edge.jarak)
        reverse_edge.is_active = edge.is_active
        self.adjacency_list[edge.tujuan].append(reverse_edge)
        
        self.total_edges += 1
    
    def load_from_csv(self, nodes_file: str, edges_file: str) -> None:
        """
        Load data graph dari file CSV.
        
        Args:
            nodes_file: Path ke file nodes.csv
            edges_file: Path ke file edges.csv
        """
        import csv
        
        # Load nodes
        print("Loading nodes dari CSV...")
        with open(nodes_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                node = Node(row['id'], row['nama_node'], row['kategori'])
                self.add_node(node)
        
        print(f"✓ Berhasil load {self.total_nodes} node")
        
        # Load edges
        print("Loading edges dari CSV...")
        with open(edges_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                edge = Edge(row['asal'], row['tujuan'], int(row['jarak']))
                self.add_edge(edge)
        
        print(f"✓ Berhasil load {self.total_edges} edge")
    
    def get_neighbors(self, node_id: str) -> List[Edge]:
        """
        Return daftar edge (neighbors) dari node tertentu.
        
        Args:
            node_id: ID node yang dicari
            
        Returns:
            List berisi Edge yang terhubung dengan node
        """
        if node_id not in self.adjacency_list:
            return []
        return self.adjacency_list[node_id]
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """
        Dapatkan object Node berdasarkan ID.
        
        Args:
            node_id: ID node yang dicari
            
        Returns:
            Object Node atau None jika tidak ditemukan
        """
        return self.nodes.get(node_id)
    
    def display_all_nodes(self) -> None:
        """Tampilkan semua node dalam format tabel."""
        print("\n" + "="*70)
        print("DAFTAR SEMUA NODE")
        print("="*70)
        print(f"{'ID':<5} {'Nama Node':<35} {'Kategori':<20}")
        print("-"*70)
        
        for node_id in sorted(self.nodes.keys()):
            node = self.nodes[node_id]
            print(f"{node.id:<5} {node.nama:<35} {node.kategori:<20}")
        
        print("-"*70)
        print(f"Total Node: {self.total_nodes}\n")
    
    def display_all_edges(self) -> None:
        """Tampilkan semua edge dalam format tabel."""
        print("\n" + "="*80)
        print("DAFTAR SEMUA EDGE (JALUR)")
        print("="*80)
        print(f"{'Asal':<8} {'Tujuan':<8} {'Jarak (m)':<12} {'Status':<15}")
        print("-"*80)
        
        # Untuk menghindari duplikat, hanya tampilkan edge satu arah
        shown_edges = set()
        
        for node_id in sorted(self.adjacency_list.keys()):
            for edge in self.adjacency_list[node_id]:
                # Buat key untuk cek duplikat (dengan sorting untuk undirected)
                edge_key = tuple(sorted([edge.asal, edge.tujuan]))
                
                if edge_key not in shown_edges:
                    shown_edges.add(edge_key)
                    status = "✓ AKTIF" if edge.is_active else "✗ TERTUTUP"
                    print(f"{edge.asal:<8} {edge.tujuan:<8} {edge.jarak:<12} {status:<15}")
        
        print("-"*80)
        print(f"Total Edge: {self.total_edges // 2}\n")  # Dibagi 2 karena undirected
    
    def close_edge(self, asal: str, tujuan: str) -> bool:
        """
        Tutup edge tertentu (simulasi kebakaran).
        
        Args:
            asal: ID node asal
            tujuan: ID node tujuan
            
        Returns:
            True jika berhasil ditutup, False jika edge tidak ditemukan
        """
        # Tutup di kedua arah
        closed_count = 0
        
        # Tutup asal→tujuan
        for edge in self.adjacency_list.get(asal, []):
            if edge.tujuan == tujuan:
                edge.close()
                closed_count += 1
        
        # Tutup tujuan→asal
        for edge in self.adjacency_list.get(tujuan, []):
            if edge.asal == asal:
                edge.close()
                closed_count += 1
        
        return closed_count > 0
    
    def open_edge(self, asal: str, tujuan: str) -> bool:
        """
        Buka kembali edge yang tertutup.
        
        Args:
            asal: ID node asal
            tujuan: ID node tujuan
            
        Returns:
            True jika berhasil dibuka, False jika edge tidak ditemukan
        """
        opened_count = 0
        
        for edge in self.adjacency_list.get(asal, []):
            if edge.tujuan == tujuan:
                edge.open()
                opened_count += 1
        
        for edge in self.adjacency_list.get(tujuan, []):
            if edge.asal == asal:
                edge.open()
                opened_count += 1
        
        return opened_count > 0
    
    def get_stats(self) -> Dict:
        """Return statistik graph."""
        return {
            'total_nodes': self.total_nodes,
            'total_edges': self.total_edges // 2,  # Undirected
            'node_categories': self._count_categories(),
            'average_degree': self.total_edges / self.total_nodes if self.total_nodes > 0 else 0
        }
    
    def _count_categories(self) -> Dict[str, int]:
        """Hitung jumlah node per kategori."""
        categories = {}
        for node in self.nodes.values():
            categories[node.kategori] = categories.get(node.kategori, 0) + 1
        return categories
    
    def __repr__(self) -> str:
        """String representation untuk debugging."""
        return f"Graph(nodes={self.total_nodes}, edges={self.total_edges})"

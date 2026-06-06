"""
evacuation.py - Sistem Evakuasi Kebakaran

Module ini berisi class EvacuationSystem yang mengintegrasikan
Graph dan Dijkstra untuk simulasi evakuasi kebakaran.

Fitur:
- Load graph dari CSV
- Input lokasi awal dan titik evakuasi
- Hitung rute evakuasi optimal
- Simulasi jalur tertutup (kebakaran)
- Bandingkan rute sebelum dan sesudah
- Test scenario

Author: Data Structure Project
"""

from typing import Dict, List, Tuple, Optional
from graph import Graph
from dijkstra import Dijkstra


class EvacuationSystem:
    """
    Sistem utama untuk evakuasi kebakaran.
    
    Mengintegrasikan struktur data Graph dan algoritma Dijkstra
    untuk menghitung rute evakuasi yang optimal dan simulasi
    jalur yang tertutup akibat kebakaran.
    
    Attributes:
        graph (Graph): Representasi jaringan gang dan fasilitas
        dijkstra (Dijkstra): Algoritma untuk shortest path
        evacuation_points (List[str]): Daftar titik evakuasi (T, U, V)
        current_start (str): Lokasi awal pengguna
        current_target (str): Titik evakuasi yang dipilih
        path_history (List[Dict]): Riwayat rute yang dihitung
    """
    
    def __init__(self) -> None:
        """Inisialisasi sistem evakuasi."""
        self.graph = Graph()
        self.dijkstra: Optional[Dijkstra] = None
        self.evacuation_points = ["T", "U", "V"]  # 3 titik evakuasi
        self.current_start: Optional[str] = None
        self.current_target: Optional[str] = None
        self.path_history: List[Dict] = []
    
    def load_graph(self, nodes_file: str, edges_file: str) -> None:
        """
        Load graph dari file CSV.
        
        Args:
            nodes_file: Path ke nodes.csv
            edges_file: Path ke edges.csv
        """
        print("\n" + "="*70)
        print("LOADING GRAPH")
        print("="*70)
        
        try:
            self.graph.load_from_csv(nodes_file, edges_file)
            self.dijkstra = Dijkstra(self.graph)
            print("✓ Graph berhasil di-load!")
            self.display_graph_info()
        except FileNotFoundError as e:
            print(f"✗ Error: File tidak ditemukan - {e}")
            raise
        except Exception as e:
            print(f"✗ Error: {e}")
            raise
    
    def display_graph_info(self) -> None:
        """Tampilkan informasi umum graph."""
        stats = self.graph.get_stats()
        print(f"\nStatistik Graph:")
        print(f"  - Total Node: {stats['total_nodes']}")
        print(f"  - Total Edge: {stats['total_edges']}")
        print(f"  - Titik Evakuasi: {len(self.evacuation_points)} (T, U, V)")
        print(f"\nKategori Node:")
        for category, count in stats['node_categories'].items():
            print(f"  - {category}: {count}")
    
    def set_start_location(self, node_id: str) -> bool:
        """
        Set lokasi awal pengguna.
        
        Args:
            node_id: ID node awal
            
        Returns:
            True jika berhasil, False jika node tidak ada
        """
        if node_id not in self.graph.nodes:
            print(f"✗ Error: Node '{node_id}' tidak ditemukan!")
            return False
        
        self.current_start = node_id
        node = self.graph.get_node(node_id)
        print(f"✓ Lokasi awal: {node.get_info()}")
        return True
    
    def set_evacuation_point(self, node_id: str) -> bool:
        """
        Set titik evakuasi.
        
        Args:
            node_id: ID node titik evakuasi
            
        Returns:
            True jika berhasil, False jika bukan titik evakuasi
        """
        if node_id not in self.evacuation_points:
            print(f"✗ Error: '{node_id}' bukan titik evakuasi yang valid!")
            print(f"  Pilih salah satu: {', '.join(self.evacuation_points)}")
            return False
        
        if node_id not in self.graph.nodes:
            print(f"✗ Error: Node '{node_id}' tidak ditemukan!")
            return False
        
        self.current_target = node_id
        node = self.graph.get_node(node_id)
        print(f"✓ Titik Evakuasi: {node.get_info()}")
        return True
    
    def calculate_evacuation_route(self) -> Tuple[List[str], float]:
        """
        Hitung rute evakuasi optimal dari start ke target.
        
        Returns:
            Tuple (rute: List[str], jarak: float)
            Contoh: (['A', 'C', 'G', 'M', 'T'], 290)
        """
        if not self.current_start:
            print("✗ Error: Lokasi awal belum diset!")
            return [], 0
        
        if not self.current_target:
            print("✗ Error: Titik evakuasi belum diset!")
            return [], 0
        
        # Hitung rute menggunakan Dijkstra
        route = self.dijkstra.find_shortest_path(self.current_start, self.current_target)
        distance = self.dijkstra.get_distance(self.current_start, self.current_target)
        
        return route, distance
    
    def display_route_info(self) -> None:
        """Tampilkan informasi rute evakuasi lengkap."""
        route, distance = self.calculate_evacuation_route()
        
        if not route:
            print("\n" + "="*70)
            print("HASIL PERHITUNGAN RUTE EVAKUASI")
            print("="*70)
            print("✗ TIDAK ADA JALUR AMAN!")
            print(f"  Dari: {self.current_start}")
            print(f"  Ke: {self.current_target}")
            print("  Rekomendasi: Arahkan ke Jalan Utama (A, B, W, X, Y)")
            print("="*70 + "\n")
            return
        
        print("\n" + "="*70)
        print("HASIL PERHITUNGAN RUTE EVAKUASI")
        print("="*70)
        
        print(f"\nLokasi Awal:")
        start_node = self.graph.get_node(self.current_start)
        print(f"  {start_node.get_info()}")
        
        print(f"\nTitik Evakuasi:")
        target_node = self.graph.get_node(self.current_target)
        print(f"  {target_node.get_info()}")
        
        print(f"\nJalur Evakuasi:")
        route_str = " → ".join(route)
        print(f"  {route_str}")
        
        print(f"\nTotal Jarak:")
        print(f"  {int(distance)} Meter")
        
        print(f"\nStatus:")
        print(f"  ✓ BERHASIL - Jalur Aman Ditemukan")
        
        print("="*70 + "\n")
        
        # Simpan ke history
        self.path_history.append({
            'start': self.current_start,
            'target': self.current_target,
            'route': route,
            'distance': distance,
            'closed_edges': []
        })
    
    def simulate_closed_path(self, asal: str, tujuan: str) -> None:
        """
        Simulasi jalur yang tertutup akibat kebakaran.
        
        Menutup edge spesifik dan menghitung ulang rute.
        
        Args:
            asal: ID node asal edge yang ditutup
            tujuan: ID node tujuan edge yang ditutup
        """
        success = self.graph.close_edge(asal, tujuan)
        
        if not success:
            print(f"✗ Edge {asal}→{tujuan} tidak ditemukan!")
            return
        
        print(f"\n✗ SIMULASI KEBAKARAN:")
        print(f"  Jalur {asal}→{tujuan} TERTUTUP")
        
        # Hitung ulang rute
        route, distance = self.calculate_evacuation_route()
        
        if route:
            print(f"\n✓ RUTE ALTERNATIF DITEMUKAN:")
            route_str = " → ".join(route)
            print(f"  {route_str}")
            print(f"  Total Jarak: {int(distance)} Meter")
        else:
            print(f"\n✗ TIDAK ADA JALUR AMAN!")
            print(f"  Rekomendasi: Arahkan ke Jalan Utama (A, B, W, X, Y)")
        
        # Simpan ke history dengan closed edges
        self.path_history[-1]['closed_edges'].append((asal, tujuan))
    
    def display_comparison(self) -> None:
        """Tampilkan perbandingan rute sebelum dan sesudah jalur tertutup."""
        if len(self.path_history) < 1:
            print("✗ Belum ada history rute untuk dibandingkan!")
            return
        
        last_record = self.path_history[-1]
        
        print("\n" + "="*70)
        print("PERBANDINGAN RUTE EVAKUASI")
        print("="*70)
        
        print(f"\nLokasi Awal: {last_record['start']}")
        print(f"Titik Evakuasi: {last_record['target']}")
        
        print(f"\n--- SEBELUM JALUR TERTUTUP ---")
        route_str = " → ".join(last_record['route'])
        print(f"Jalur: {route_str}")
        print(f"Jarak: {int(last_record['distance'])} Meter")
        
        if last_record['closed_edges']:
            print(f"\n--- JALUR YANG TERTUTUP ---")
            for asal, tujuan in last_record['closed_edges']:
                print(f"  ✗ {asal} → {tujuan}")
            
            # Hitung ulang rute baru
            new_route, new_distance = self.calculate_evacuation_route()
            
            print(f"\n--- SESUDAH JALUR TERTUTUP ---")
            if new_route:
                new_route_str = " → ".join(new_route)
                print(f"Jalur: {new_route_str}")
                print(f"Jarak: {int(new_distance)} Meter")
                
                # Hitung perubahan
                distance_change = int(new_distance) - int(last_record['distance'])
                print(f"\nPerubahan Jarak: +{distance_change} Meter")
            else:
                print(f"Jalur: TIDAK ADA JALUR AMAN!")
        
        print("="*70 + "\n")
    
    def run_interactive_mode(self) -> None:
        """Jalankan mode interaktif untuk input user."""
        print("\n" + "="*70)
        print("MODE INTERAKTIF - SISTEM EVAKUASI KEBAKARAN")
        print("="*70)
        
        while True:
            print("\nMenu Utama:")
            print("1. Cari Rute Evakuasi")
            print("2. Simulasi Jalur Tertutup (Kebakaran)")
            print("3. Lihat Perbandingan Rute")
            print("4. Tampilkan Semua Node")
            print("5. Tampilkan Semua Edge")
            print("6. Keluar")
            
            choice = input("\nPilih menu (1-6): ").strip()
            
            if choice == "1":
                self._interactive_find_route()
            elif choice == "2":
                self._interactive_simulate_fire()
            elif choice == "3":
                self.display_comparison()
            elif choice == "4":
                self.graph.display_all_nodes()
            elif choice == "5":
                self.graph.display_all_edges()
            elif choice == "6":
                print("\n✓ Program selesai. Terima kasih!")
                break
            else:
                print("✗ Input tidak valid!")
    
    def _interactive_find_route(self) -> None:
        """Interactive: Cari rute evakuasi."""
        print("\n--- CARI RUTE EVAKUASI ---")
        
        # Input lokasi awal
        start = input("Masukkan lokasi awal (A-Y): ").strip().upper()
        if not self.set_start_location(start):
            return
        
        # Input titik evakuasi
        print(f"\nTitik Evakuasi yang tersedia:")
        for point in self.evacuation_points:
            node = self.graph.get_node(point)
            print(f"  {point}: {node.nama}")
        
        target = input("Pilih titik evakuasi: ").strip().upper()
        if not self.set_evacuation_point(target):
            return
        
        # Display rute
        self.display_route_info()
    
    def _interactive_simulate_fire(self) -> None:
        """Interactive: Simulasi jalur tertutup."""
        print("\n--- SIMULASI KEBAKARAN ---")
        
        # Reset untuk simulasi baru
        if not self.path_history or not self.current_start or not self.current_target:
            print("Jalankan 'Cari Rute' dulu sebelum simulasi!")
            return
        
        asal = input("Node asal jalur yang tertutup: ").strip().upper()
        tujuan = input("Node tujuan jalur yang tertutup: ").strip().upper()
        
        self.simulate_closed_path(asal, tujuan)
    
    def run_test_scenario(self, scenario: Dict) -> Dict:
        """
        Jalankan test scenario dan return hasil.
        
        Args:
            scenario: Dict berisi:
                - 'start': Node awal
                - 'target': Node tujuan
                - 'closed_edges': List of (asal, tujuan) yang ditutup
        
        Returns:
            Dict hasil berisi:
                - 'start': Node awal
                - 'target': Node tujuan
                - 'initial_route': Rute sebelum jalur ditutup
                - 'initial_distance': Jarak sebelum
                - 'closed_edges': Jalur yang ditutup
                - 'final_route': Rute setelah jalur ditutup
                - 'final_distance': Jarak setelah
                - 'status': 'BERHASIL' atau 'GAGAL'
        """
        result = {
            'start': scenario['start'],
            'target': scenario['target'],
            'initial_route': [],
            'initial_distance': 0,
            'closed_edges': scenario.get('closed_edges', []),
            'final_route': [],
            'final_distance': 0,
            'status': 'GAGAL'
        }
        
        # Set lokasi
        if not self.set_start_location(scenario['start']):
            return result
        
        if not self.set_evacuation_point(scenario['target']):
            return result
        
        # Hitung rute awal
        initial_route, initial_distance = self.calculate_evacuation_route()
        
        if not initial_route:
            return result
        
        result['initial_route'] = initial_route
        result['initial_distance'] = initial_distance
        
        # Simulasi jalur tertutup
        for asal, tujuan in scenario.get('closed_edges', []):
            self.graph.close_edge(asal, tujuan)
        
        # Hitung rute final
        final_route, final_distance = self.calculate_evacuation_route()
        
        if final_route:
            result['final_route'] = final_route
            result['final_distance'] = final_distance
            result['status'] = 'BERHASIL'
        else:
            result['status'] = 'GAGAL'
        
        # Buka kembali edge untuk test berikutnya
        for asal, tujuan in scenario.get('closed_edges', []):
            self.graph.open_edge(asal, tujuan)
        
        return result
    
    def display_test_results(self, results: List[Dict], title: str) -> None:
        """Tampilkan hasil test dalam format tabel."""
        print("\n" + "="*100)
        print(title)
        print("="*100)
        print(f"{'No':<4} {'Start':<8} {'Target':<8} {'Status':<12} "
              f"{'Jarak Awal':<12} {'Jarak Akhir':<12}")
        print("-"*100)
        
        for i, result in enumerate(results, 1):
            status = result['status']
            initial = int(result['initial_distance'])
            final = int(result['final_distance']) if result['final_route'] else "N/A"
            
            print(f"{i:<4} {result['start']:<8} {result['target']:<8} "
                  f"{status:<12} {initial:<12} {final:<12}")
        
        print("-"*100 + "\n")
    
    def __repr__(self) -> str:
        """String representation untuk debugging."""
        return f"EvacuationSystem(graph={self.graph})"

"""
main.py - Program Utama Sistem Evakuasi Kebakaran

Program ini adalah entry point untuk sistem evakuasi kebakaran.
Menghubungkan semua modul (graph, dijkstra, evacuation) dan
menyediakan interface user.

Author: Data Structure Project
"""

import os
from evacuation import EvacuationSystem


def print_welcome():
    """Tampilkan welcome banner."""
    print("\n" + "="*70)
    print("SISTEM EVAKUASI KEBAKARAN")
    print("Implementasi Graph dan Algoritma Dijkstra")
    print("="*70)
    print("\nStudi Kasus: Kelurahan Kapasari/Simolawang,")
    print("Kecamatan Simokerto, Surabaya")
    print("\nProyek Mata Kuliah: Struktur Data")
    print("="*70 + "\n")


def get_csv_path(filename: str) -> str:
    """
    Dapatkan path file CSV relative atau absolute.
    
    Args:
        filename: Nama file (nodes.csv atau edges.csv)
        
    Returns:
        Path lengkap ke file
    """
    # Coba beberapa path
    possible_paths = [
        f"data/{filename}",
        f"./data/{filename}",
        f"../data/{filename}",
        os.path.join(os.path.dirname(__file__), "..", "data", filename),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Default ke path pertama jika tidak ditemukan
    return possible_paths[0]


def main():
    """Program utama."""
    print_welcome()
    
    # Inisialisasi sistem
    system = EvacuationSystem()
    
    # Load graph dari CSV
    nodes_file = get_csv_path("nodes.csv")
    edges_file = get_csv_path("edges.csv")
    
    try:
        system.load_graph(nodes_file, edges_file)
    except FileNotFoundError:
        print("\n✗ Error: File CSV tidak ditemukan!")
        print(f"  Pastikan file ada di lokasi:")
        print(f"  - {nodes_file}")
        print(f"  - {edges_file}")
        return
    
    # Menu utama
    while True:
        print("\n" + "="*70)
        print("MENU UTAMA")
        print("="*70)
        print("1. Mode Interaktif (Input user)")
        print("2. Jalankan 5 Skenario Normal")
        print("3. Jalankan 5 Skenario Jalur Tertutup")
        print("4. Tampilkan Informasi Graph")
        print("5. DEMO: Operasi DELETE (INSERT/DELETE/TRAVERSAL)")
        print("6. Keluar")
        print("="*70)
        
        choice = input("\nPilih menu (1-6): ").strip()
        
        if choice == "1":
            system.run_interactive_mode()
        
        elif choice == "2":
            run_normal_scenarios(system)
        
        elif choice == "3":
            run_closed_path_scenarios(system)
        
        elif choice == "4":
            show_graph_info(system)
        
        elif choice == "5":
            demonstrate_delete_operations(system)
        
        elif choice == "6":
            print("\n✓ Program selesai. Terima kasih!\n")
            break
        
        else:
            print("✗ Input tidak valid!")


def run_normal_scenarios(system: EvacuationSystem) -> None:
    """Jalankan 5 skenario normal (tanpa jalur tertutup)."""
    print("\n" + "="*70)
    print("5 SKENARIO NORMAL - JALUR TERSEDIA")
    print("="*70)
    
    scenarios = [
        {'start': 'C', 'target': 'T', 'closed_edges': []},
        {'start': 'G', 'target': 'U', 'closed_edges': []},
        {'start': 'M', 'target': 'T', 'closed_edges': []},
        {'start': 'E', 'target': 'V', 'closed_edges': []},
        {'start': 'H', 'target': 'T', 'closed_edges': []},
    ]
    
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n--- SKENARIO {i} ---")
        print(f"Dari: {scenario['start']} → Ke: {scenario['target']}")
        
        result = system.run_test_scenario(scenario)
        results.append(result)
        
        if result['status'] == 'BERHASIL':
            route_str = " → ".join(result['initial_route'])
            distance = int(result['initial_distance'])
            print(f"✓ Jalur: {route_str}")
            print(f"  Jarak: {distance} Meter")
        else:
            print(f"✗ Tidak ada jalur aman!")
    
    # Tampilkan tabel ringkasan
    system.display_test_results(results, "RINGKASAN 5 SKENARIO NORMAL")


def run_closed_path_scenarios(system: EvacuationSystem) -> None:
    """Jalankan 5 skenario dengan jalur tertutup."""
    print("\n" + "="*70)
    print("5 SKENARIO JALUR TERTUTUP - SIMULASI KEBAKARAN")
    print("="*70)
    
    scenarios = [
        {
            'start': 'C',
            'target': 'T',
            'closed_edges': [('C', 'D')],  # Tutup C→D
            'description': 'Jalur C→D tertutup'
        },
        {
            'start': 'G',
            'target': 'U',
            'closed_edges': [('G', 'H')],  # Tutup G→H
            'description': 'Jalur G→H tertutup'
        },
        {
            'start': 'M',
            'target': 'T',
            'closed_edges': [('M', 'N')],  # Tutup M→N
            'description': 'Jalur M→N tertutup'
        },
        {
            'start': 'E',
            'target': 'V',
            'closed_edges': [('D', 'E')],  # Tutup D→E
            'description': 'Jalur D→E tertutup'
        },
        {
            'start': 'H',
            'target': 'T',
            'closed_edges': [('H', 'I')],  # Tutup H→I
            'description': 'Jalur H→I tertutup'
        },
    ]
    
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n--- SKENARIO {i} ---")
        print(f"Dari: {scenario['start']} → Ke: {scenario['target']}")
        print(f"Situasi: {scenario['description']}")
        
        result = system.run_test_scenario(scenario)
        results.append(result)
        
        print(f"\nRute Awal (sebelum tertutup):")
        if result['initial_route']:
            route_str = " → ".join(result['initial_route'])
            print(f"  {route_str} ({int(result['initial_distance'])} m)")
        else:
            print(f"  Tidak ada rute")
        
        print(f"\nJalur Tertutup:")
        for asal, tujuan in result['closed_edges']:
            print(f"  ✗ {asal} → {tujuan}")
        
        print(f"\nRute Alternatif (sesudah tertutup):")
        if result['final_route']:
            route_str = " → ".join(result['final_route'])
            distance_change = int(result['final_distance']) - int(result['initial_distance'])
            print(f"  {route_str} ({int(result['final_distance'])} m)")
            print(f"  Perubahan jarak: +{distance_change} m")
            print(f"  ✓ Status: {result['status']}")
        else:
            print(f"  Tidak ada jalur alternatif!")
            print(f"  ✗ Status: {result['status']}")
    
    # Tampilkan tabel ringkasan
    system.display_test_results(results, "RINGKASAN 5 SKENARIO JALUR TERTUTUP")


def show_graph_info(system: EvacuationSystem) -> None:
    """Tampilkan informasi lengkap graph."""
    print("\n" + "="*70)
    print("INFORMASI GRAPH")
    print("="*70)
    
    # Tampilkan statistik
    system.display_graph_info()
    
    # Menu sub
    while True:
        print("\nMenu Informasi:")
        print("1. Tampilkan semua node")
        print("2. Tampilkan semua edge")
        print("3. Kembali ke menu utama")
        
        choice = input("\nPilih (1-3): ").strip()
        
        if choice == "1":
            system.graph.display_all_nodes()
        elif choice == "2":
            system.graph.display_all_edges()
        elif choice == "3":
            break
        else:
            print("✗ Input tidak valid!")


def demonstrate_delete_operations(system: EvacuationSystem) -> None:
    """
    DEMONSTRASI LENGKAP: 3 Operasi yang Diwajibkan
    1. INSERT Operation (Menambah data)
    2. DELETE Operation (Menghapus data)
    3. TRAVERSAL Operation (Akses/cari data)
    """
    print("\n" + "="*70)
    print("DEMONSTRASI OPERASI DATA - CRUD OPERATIONS")
    print("="*70)
    print("\nMenampilkan 3 operasi yang diwajibkan:")
    print("  1️⃣  INSERT - Menambahkan data (add_node, add_edge)")
    print("  2️⃣  DELETE - Menghapus data (remove_node, remove_edge)")
    print("  3️⃣  TRAVERSAL - Akses/Cari data (get_neighbors, display)")
    
    while True:
        print("\n" + "="*70)
        print("MENU DEMONSTRASI DELETE OPERATIONS")
        print("="*70)
        print("\n📝 OPERASI YANG AKAN KAMI DEMONSTRASIKAN:")
        print("\n1️⃣  OPERASI INSERT (CREATE)")
        print("   - Membuat node baru")
        print("   - Menambahkan edge baru")
        print("\n2️⃣  OPERASI DELETE (REMOVE)")
        print("   - Menghapus edge secara permanen")
        print("   - Menghapus node beserta semua edges-nya")
        print("   - BEDA: close_edge (marking) vs remove_edge (hapus selamanya)")
        print("\n3️⃣  OPERASI TRAVERSAL (READ)")
        print("   - Menampilkan semua nodes")
        print("   - Menampilkan semua edges")
        print("   - Mencari neighbors dari node tertentu")
        
        print("\n" + "-"*70)
        print("Pilih Demonstrasi:")
        print("-"*70)
        print("1. Demo: INSERT Node (Membuat Node Baru)")
        print("2. Demo: INSERT Edge (Membuat Koneksi Baru)")
        print("3. Demo: TRAVERSAL - Lihat Semua Node")
        print("4. Demo: TRAVERSAL - Lihat Semua Edge")
        print("5. Demo: DELETE Edge (Hapus Koneksi Secara Permanen)")
        print("6. Demo: DELETE Node (Hapus Node + Semua Koneksinya)")
        print("7. Demo: Perbedaan close_edge vs remove_edge")
        print("8. Kembali ke Menu Utama")
        print("="*70)
        
        choice = input("\nPilih demonstrasi (1-8): ").strip()
        
        if choice == "1":
            demo_insert_node(system)
        elif choice == "2":
            demo_insert_edge(system)
        elif choice == "3":
            demo_traversal_nodes(system)
        elif choice == "4":
            demo_traversal_edges(system)
        elif choice == "5":
            demo_delete_edge(system)
        elif choice == "6":
            demo_delete_node(system)
        elif choice == "7":
            demo_close_vs_remove(system)
        elif choice == "8":
            break
        else:
            print("✗ Input tidak valid!")


def demo_insert_node(system: EvacuationSystem) -> None:
    """Demo: INSERT - Menambahkan Node Baru"""
    from graph import Node
    
    print("\n" + "="*70)
    print("DEMO 1️⃣  OPERASI INSERT - MENAMBAHKAN NODE BARU")
    print("="*70)
    
    print("\n📌 Sebelum menambah node:")
    print(f"   Total nodes: {system.graph.total_nodes}")
    
    # Buat node baru
    new_node_id = "Z"
    new_node = Node(new_node_id, "Titik Evakuasi Baru", "Titik Evakuasi")
    
    print(f"\n📝 Membuat node baru: {new_node.get_info()}")
    print(f"   Code: graph.add_node(node)")
    
    # Tambahkan node
    system.graph.add_node(new_node)
    
    print(f"\n✅ Node berhasil ditambahkan!")
    print(f"   Total nodes sekarang: {system.graph.total_nodes}")
    print(f"   Node '{new_node_id}' sudah ada di graph ✓")
    
    input("\nTekan Enter untuk lanjut...")


def demo_insert_edge(system: EvacuationSystem) -> None:
    """Demo: INSERT - Menambahkan Edge Baru"""
    from graph import Edge
    
    print("\n" + "="*70)
    print("DEMO 2️⃣  OPERASI INSERT - MENAMBAHKAN EDGE (KONEKSI) BARU")
    print("="*70)
    
    print("\n📌 Sebelum menambah edge:")
    print(f"   Total edges: {system.graph.total_edges}")
    
    # Tanyakan node untuk dihubungkan
    print("\n📍 Tersedia node: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z")
    
    asal = input("Pilih node asal (contoh: A): ").strip().upper()
    if asal not in system.graph.nodes:
        print(f"❌ Node '{asal}' tidak ditemukan!")
        return
    
    tujuan = input("Pilih node tujuan (contoh: B): ").strip().upper()
    if tujuan not in system.graph.nodes:
        print(f"❌ Node '{tujuan}' tidak ditemukan!")
        return
    
    jarak = input("Masukkan jarak dalam meter (contoh: 100): ").strip()
    try:
        jarak = int(jarak)
    except ValueError:
        print("❌ Jarak harus berupa angka!")
        return
    
    # Buat dan tambahkan edge
    new_edge = Edge(asal, tujuan, jarak)
    
    print(f"\n📝 Membuat edge baru: {asal} ↔ {tujuan} ({jarak}m)")
    print(f"   Code: graph.add_edge(edge)")
    
    try:
        system.graph.add_edge(new_edge)
        print(f"\n✅ Edge berhasil ditambahkan!")
        print(f"   Total edges sekarang: {system.graph.total_edges}")
        print(f"   Koneksi {asal} ↔ {tujuan} sudah aktif ✓")
    except ValueError as e:
        print(f"❌ Error: {e}")
    
    input("\nTekan Enter untuk lanjut...")


def demo_traversal_nodes(system: EvacuationSystem) -> None:
    """Demo: TRAVERSAL - Menampilkan Semua Node"""
    print("\n" + "="*70)
    print("DEMO 3️⃣  OPERASI TRAVERSAL - MENAMPILKAN SEMUA NODE")
    print("="*70)
    
    print("\n📌 Mengakses dan menampilkan data graph:")
    print("   Code: graph.display_all_nodes()")
    print("   Operasi: TRAVERSAL - Iterasi semua nodes dan tampilkan")
    
    system.graph.display_all_nodes()
    
    input("Tekan Enter untuk lanjut...")


def demo_traversal_edges(system: EvacuationSystem) -> None:
    """Demo: TRAVERSAL - Menampilkan Semua Edge"""
    print("\n" + "="*70)
    print("DEMO 4️⃣  OPERASI TRAVERSAL - MENAMPILKAN SEMUA EDGE")
    print("="*70)
    
    print("\n📌 Mengakses dan menampilkan semua edges:")
    print("   Code: graph.display_all_edges()")
    print("   Operasi: TRAVERSAL - Iterasi semua edges dan tampilkan")
    
    system.graph.display_all_edges()
    
    input("Tekan Enter untuk lanjut...")


def demo_delete_edge(system: EvacuationSystem) -> None:
    """Demo: DELETE - Menghapus Edge Secara Permanen"""
    print("\n" + "="*70)
    print("DEMO 5️⃣  OPERASI DELETE - MENGHAPUS EDGE SECARA PERMANEN")
    print("="*70)
    
    print("\n📌 Sebelum menghapus edge:")
    print(f"   Total edges: {system.graph.total_edges}")
    
    # Tanyakan edge yang akan dihapus
    print("\n📍 Pilih edge yang akan dihapus:")
    asal = input("Node asal (contoh: C): ").strip().upper()
    if asal not in system.graph.nodes:
        print(f"❌ Node '{asal}' tidak ditemukan!")
        return
    
    tujuan = input("Node tujuan (contoh: D): ").strip().upper()
    if tujuan not in system.graph.nodes:
        print(f"❌ Node '{tujuan}' tidak ditemukan!")
        return
    
    neighbors = [e.tujuan for e in system.graph.get_neighbors(asal)]
    if tujuan not in neighbors:
        print(f"❌ Tidak ada edge antara {asal} dan {tujuan}!")
        return
    
    print(f"\n📝 Menghapus edge: {asal} ↔ {tujuan}")
    print(f"   Code: graph.remove_edge('{asal}', '{tujuan}')")
    print(f"   Catatan: Edge BENAR-BENAR DIHAPUS, bukan hanya ditutup!")
    
    # Hapus edge
    edges_before = system.graph.total_edges
    result = system.graph.remove_edge(asal, tujuan)
    
    if result:
        print(f"\n✅ Edge berhasil dihapus!")
        print(f"   Edges sebelum: {edges_before}")
        print(f"   Edges sekarang: {system.graph.total_edges}")
        print(f"   Neighbors {asal} sekarang: {[e.tujuan for e in system.graph.get_neighbors(asal)]}")
        print(f"   Neighbors {tujuan} sekarang: {[e.tujuan for e in system.graph.get_neighbors(tujuan)]}")
    else:
        print(f"❌ Edge tidak ditemukan!")
    
    input("\nTekan Enter untuk lanjut...")


def demo_delete_node(system: EvacuationSystem) -> None:
    """Demo: DELETE - Menghapus Node Beserta Edges-nya"""
    print("\n" + "="*70)
    print("DEMO 6️⃣  OPERASI DELETE - MENGHAPUS NODE + SEMUA KONEKSINYA")
    print("="*70)
    
    print("\n📌 Sebelum menghapus node:")
    print(f"   Total nodes: {system.graph.total_nodes}")
    print(f"   Total edges: {system.graph.total_edges}")
    
    # Tanyakan node yang akan dihapus
    print("\n⚠️  Peringatan: Operasi ini akan menghapus node dan SEMUA edges-nya!")
    print("    Pilih node yang tidak penting untuk demo (tidak untuk data utama).")
    
    node_id = input("\nMasukkan ID node untuk dihapus (contoh: Z): ").strip().upper()
    if node_id not in system.graph.nodes:
        print(f"❌ Node '{node_id}' tidak ditemukan!")
        return
    
    # Tampilkan info node sebelum dihapus
    neighbors_before = [e.tujuan for e in system.graph.get_neighbors(node_id)]
    print(f"\n📝 Info node sebelum dihapus:")
    print(f"   Node: {node_id}")
    print(f"   Neighbors: {neighbors_before} (total: {len(neighbors_before)} koneksi)")
    
    print(f"\n📝 Menghapus node: {node_id}")
    print(f"   Code: graph.remove_node('{node_id}')")
    print(f"   Aksi: Hapus node + semua edges yang terhubung")
    
    # Hapus node
    nodes_before = system.graph.total_nodes
    edges_before = system.graph.total_edges
    result = system.graph.remove_node(node_id)
    
    if result:
        print(f"\n✅ Node berhasil dihapus!")
        print(f"   Nodes sebelum: {nodes_before} → sekarang: {system.graph.total_nodes}")
        print(f"   Edges sebelum: {edges_before} → sekarang: {system.graph.total_edges}")
        print(f"   ✓ Node '{node_id}' dan semua koneksinya sudah dihapus")
    else:
        print(f"❌ Node tidak ditemukan!")
    
    input("\nTekan Enter untuk lanjut...")


def demo_close_vs_remove(system: EvacuationSystem) -> None:
    """Demo: Perbedaan close_edge (marking) vs remove_edge (delete)"""
    print("\n" + "="*70)
    print("DEMO 7️⃣  PERBEDAAN: close_edge() vs remove_edge()")
    print("="*70)
    
    print("\n📌 OPERASI YANG BERBEDA:")
    print("\n  1️⃣  close_edge(asal, tujuan):")
    print("     - Menandai edge sebagai TIDAK AKTIF (is_active = False)")
    print("     - Edge MASIH ADA di graph")
    print("     - Total edges TIDAK BERUBAH")
    print("     - Bisa dibuka kembali dengan open_edge()")
    print("     - USE CASE: Simulasi kebakaran/jalur tertutup sementara")
    
    print("\n  2️⃣  remove_edge(asal, tujuan):")
    print("     - BENAR-BENAR MENGHAPUS edge dari graph")
    print("     - Edge TIDAK ADA lagi di graph")
    print("     - Total edges BERKURANG")
    print("     - TIDAK bisa dikembalikan")
    print("     - USE CASE: Maintenance/perbaikan permanen")
    
    print("\n" + "-"*70)
    print("DEMO PRAKTIS:")
    print("-"*70)
    
    # Pilih edge untuk demo
    print("\n📍 Pilih edge untuk demonstrasi:")
    asal = input("Node asal (contoh: C): ").strip().upper()
    if asal not in system.graph.nodes:
        print(f"❌ Node '{asal}' tidak ditemukan!")
        return
    
    neighbors = [e.tujuan for e in system.graph.get_neighbors(asal)]
    if not neighbors:
        print(f"❌ Node '{asal}' tidak punya tetangga!")
        return
    
    print(f"   Tetangga {asal}: {neighbors}")
    tujuan = input(f"Node tujuan: ").strip().upper()
    if tujuan not in neighbors:
        print(f"❌ Tidak ada edge antara {asal} dan {tujuan}!")
        return
    
    # Demo close_edge
    print(f"\n✅ STEP 1: Menggunakan close_edge('{asal}', '{tujuan}')")
    print(f"   Sebelum:")
    print(f"   - Total edges: {system.graph.total_edges}")
    edge_status_before = any(e.tujuan == tujuan for e in system.graph.get_neighbors(asal))
    print(f"   - Edge {asal}→{tujuan} aktif: {edge_status_before}")
    
    system.graph.close_edge(asal, tujuan)
    
    print(f"\n   Sesudah close_edge():")
    print(f"   - Total edges: {system.graph.total_edges} (TIDAK BERUBAH ✗)")
    edge = next((e for e in system.graph.get_neighbors(asal) if e.tujuan == tujuan), None)
    if edge:
        print(f"   - Edge {asal}→{tujuan} aktif: {edge.is_active} (hanya marking)")
        print(f"   - Edge MASIH ADA, hanya ditandai sebagai tidak aktif")
    
    # Demo open kembali
    print(f"\n✅ STEP 2: Membuka kembali dengan open_edge('{asal}', '{tujuan}')")
    system.graph.open_edge(asal, tujuan)
    edge = next((e for e in system.graph.get_neighbors(asal) if e.tujuan == tujuan), None)
    print(f"   - Edge {asal}→{tujuan} aktif sekarang: {edge.is_active} ✓")
    
    input("\nTekan Enter untuk lanjut...")


if __name__ == "__main__":
    """
    Entry point program.
    
    Jalankan dengan:
        python main.py
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Program dihentikan oleh user.")
    except Exception as e:
        print(f"\n✗ Error tidak terduga: {e}")
        import traceback
        traceback.print_exc()

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
        print("5. ⭐ DEMO: 3 OPERASI WAJIB (INSERT/DELETE/TRAVERSAL)")
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
    print("⭐ DEMONSTRASI: 3 OPERASI DATA STRUKTUR WAJIB (CRUD) ⭐")
    print("="*70)
    print("\nMenampilkan 3 operasi yang diwajibkan dalam struktur data:")
    print("  ✏️  INSERT  - Menambahkan data baru ke graph")
    print("  🗑️  DELETE  - Menghapus data permanen dari graph")
    print("  🔍 SEARCH  - Mengakses & mencari data dalam graph")
    print("\nOperasi ini disertai dengan demonstrasi praktikal yang interaktif.")
    
    while True:
        print("\n" + "="*70)
        print("MENU DEMONSTRASI CRUD OPERATIONS")
        print("="*70)
        
        print("\n┌─ ✏️  OPERASI INSERT (CREATE) ─────────────────────────────┐")
        print("│ Menambahkan data baru ke dalam graph                      │")
        print("│ 1. Demo: INSERT Node (Membuat Node Baru)                  │")
        print("│ 2. Demo: INSERT Edge (Membuat Koneksi Baru)               │")
        print("└────────────────────────────────────────────────────────────┘")
        
        print("\n┌─ 🔍 OPERASI TRAVERSAL (READ/SEARCH) ───────────────────┐")
        print("│ Mengakses dan mencari data dalam graph                    │")
        print("│ 3. Demo: TRAVERSAL - Lihat Semua Node                     │")
        print("│ 4. Demo: TRAVERSAL - Lihat Semua Edge                     │")
        print("│ 7. Demo: TRAVERSAL - Cari Neighbors dari Node Tertentu    │")
        print("└────────────────────────────────────────────────────────────┘")
        
        print("\n┌─ 🗑️  OPERASI DELETE (REMOVE) ─────────────────────────────┐")
        print("│ Menghapus data permanen dari graph                        │")
        print("│ 5. Demo: DELETE Edge (Hapus Koneksi Secara Permanen)      │")
        print("│ 6. Demo: DELETE Node (Hapus Node + Semua Koneksinya)      │")
        print("│ 8. Demo: Perbedaan close_edge vs remove_edge              │")
        print("└────────────────────────────────────────────────────────────┘")
        
        print("\n" + "-"*70)
        print("9. Kembali ke Menu Utama")
        print("="*70)
        
        choice = input("\nPilih demonstrasi (1-9): ").strip()
        
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
            demo_traversal_neighbors(system)
        elif choice == "8":
            demo_close_vs_remove(system)
        elif choice == "9":
            break
        else:
            print("✗ Input tidak valid!")


def demo_insert_node(system: EvacuationSystem) -> None:
    """Demo: INSERT - Menambahkan Node Baru"""
    from graph import Node
    
    print("\n" + "="*70)
    print("DEMO 1️⃣  OPERASI INSERT (CREATE) - MENAMBAHKAN NODE BARU")
    print("="*70)
    
    print("\n📊 STATUS GRAPH SEBELUM INSERT:")
    print(f"   Total nodes: {system.graph.total_nodes}")
    print(f"   Daftar node: {sorted(system.graph.nodes.keys())}")
    
    # Buat node baru
    new_node_id = "Z"
    new_node = Node(new_node_id, "Titik Evakuasi Baru", "Titik Evakuasi")
    
    print(f"\n📝 MEMBUAT NODE BARU:")
    print(f"   from graph import Node")
    print(f"   new_node = Node('{new_node_id}', 'Titik Evakuasi Baru', 'Titik Evakuasi')")
    print(f"   graph.add_node(new_node)")
    print(f"\n   Detail node baru:")
    print(f"   - ID: {new_node.id}")
    print(f"   - Nama: {new_node.nama}")
    print(f"   - Kategori: {new_node.kategori}")
    
    # Tambahkan node
    system.graph.add_node(new_node)
    
    print(f"\n✅ HASIL SETELAH INSERT:")
    print(f"   Total nodes: {system.graph.total_nodes}")
    print(f"   Daftar node: {sorted(system.graph.nodes.keys())}")
    print(f"   ✓ Node '{new_node_id}' BERHASIL ditambahkan ke graph!")
    print(f"\n   Catatan: Ini adalah OPERASI INSERT dalam struktur data.")
    print(f"   Data baru telah ditambahkan ke dalam graph.")
    
    input("\nTekan Enter untuk lanjut...")



def demo_insert_edge(system: EvacuationSystem) -> None:
    """Demo: INSERT - Menambahkan Edge Baru"""
    from graph import Edge
    
    print("\n" + "="*70)
    print("DEMO 2️⃣  OPERASI INSERT (CREATE) - MENAMBAHKAN EDGE (KONEKSI) BARU")
    print("="*70)
    
    print("\n📊 STATUS GRAPH SEBELUM INSERT:")
    print(f"   Total edges: {system.graph.total_edges}")
    
    # Tanyakan node untuk dihubungkan
    print("\n📍 Tersedia node: " + ", ".join(sorted(system.graph.nodes.keys())))
    
    asal = input("\nPilih node asal (contoh: A): ").strip().upper()
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
    
    print(f"\n📝 MEMBUAT EDGE BARU:")
    print(f"   from graph import Edge")
    print(f"   new_edge = Edge('{asal}', '{tujuan}', {jarak})")
    print(f"   graph.add_edge(new_edge)")
    print(f"\n   Detail edge baru:")
    print(f"   - Node asal: {asal}")
    print(f"   - Node tujuan: {tujuan}")
    print(f"   - Jarak: {jarak} meter")
    print(f"   - Status: Aktif (is_active = True)")
    print(f"   - Tipe: Undirected (bisa dilalui dua arah)")
    
    try:
        system.graph.add_edge(new_edge)
        print(f"\n✅ HASIL SETELAH INSERT:")
        print(f"   Total edges: {system.graph.total_edges}")
        print(f"   ✓ Edge berhasil ditambahkan ke graph!")
        print(f"   ✓ Koneksi {asal} ↔ {tujuan} ({jarak}m) AKTIF")
        print(f"\n   Catatan: Ini adalah OPERASI INSERT dalam struktur data.")
        print(f"   Koneksi/relasi baru telah ditambahkan ke dalam graph.")
    except ValueError as e:
        print(f"❌ Error: {e}")
    
    input("\nTekan Enter untuk lanjut...")


def demo_traversal_nodes(system: EvacuationSystem) -> None:
    """Demo: TRAVERSAL - Menampilkan Semua Node"""
    print("\n" + "="*70)
    print("DEMO 3️⃣  OPERASI TRAVERSAL (READ/SEARCH) - LIHAT SEMUA NODE")
    print("="*70)
    
    print("\n📌 Mengakses dan menampilkan semua data nodes:")
    print("   Code: graph.display_all_nodes()")
    print("   Operasi: TRAVERSAL - Iterasi (loop) semua nodes dan tampilkan")
    print("\n   Proses:")
    print("   1. Akses dictionary nodes")
    print("   2. Iterasi setiap node dalam dictionary")
    print("   3. Tampilkan informasi node (ID, Nama, Kategori)")
    
    print("\n✅ HASIL TRAVERSAL SEMUA NODE:\n")
    system.graph.display_all_nodes()
    
    print("   Catatan: Ini adalah OPERASI TRAVERSAL/SEARCH dalam struktur data.")
    print("   Kami mengakses dan membaca SEMUA data yang tersimpan di graph.")
    
    input("Tekan Enter untuk lanjut...")


def demo_traversal_edges(system: EvacuationSystem) -> None:
    """Demo: TRAVERSAL - Menampilkan Semua Edge"""
    print("\n" + "="*70)
    print("DEMO 4️⃣  OPERASI TRAVERSAL (READ/SEARCH) - LIHAT SEMUA EDGE")
    print("="*70)
    
    print("\n📌 Mengakses dan menampilkan semua data edges:")
    print("   Code: graph.display_all_edges()")
    print("   Operasi: TRAVERSAL - Iterasi (loop) semua edges dan tampilkan")
    print("\n   Proses:")
    print("   1. Akses adjacency list")
    print("   2. Iterasi setiap edge dalam adjacency list")
    print("   3. Tampilkan informasi edge (Asal, Tujuan, Jarak, Status)")
    
    print("\n✅ HASIL TRAVERSAL SEMUA EDGE:\n")
    system.graph.display_all_edges()
    
    print("   Catatan: Ini adalah OPERASI TRAVERSAL/SEARCH dalam struktur data.")
    print("   Kami mengakses dan membaca SEMUA relasi yang tersimpan di graph.")
    
    input("Tekan Enter untuk lanjut...")


def demo_traversal_neighbors(system: EvacuationSystem) -> None:
    """Demo: TRAVERSAL - Mencari Neighbors dari Node Tertentu"""
    print("\n" + "="*70)
    print("DEMO 7️⃣  OPERASI TRAVERSAL - CARI NEIGHBORS NODE")
    print("="*70)
    
    print("\n📌 Mencari dan menampilkan semua neighbors (tetangga) dari node:")
    print("   Code: graph.get_neighbors(node_id)")
    print("   Operasi: TRAVERSAL - Akses adjacency list dari node tertentu")
    
    # Tampilkan daftar node
    print("\n📍 Daftar Node yang tersedia:")
    node_list = sorted(system.graph.nodes.keys())
    print(f"   {', '.join(node_list)}")
    
    # Tanyakan node yang dicari
    node_id = input("\nMasukkan ID node untuk dicari neighbors-nya (contoh: C): ").strip().upper()
    if node_id not in system.graph.nodes:
        print(f"❌ Node '{node_id}' tidak ditemukan!")
        return
    
    # Tampilkan info node
    node = system.graph.get_node(node_id)
    print(f"\n📝 Node yang dicari:")
    print(f"   {node.get_info()}")
    
    # Ambil neighbors
    neighbors = system.graph.get_neighbors(node_id)
    
    print(f"\n✅ NEIGHBORS (Tetangga) dari Node '{node_id}':")
    print(f"   Total koneksi: {len(neighbors)}")
    
    if neighbors:
        print(f"\n   {'Tujuan':<8} {'Jarak (m)':<12} {'Status':<15}")
        print(f"   {'-'*35}")
        for edge in neighbors:
            status = "✓ AKTIF" if edge.is_active else "✗ TERTUTUP"
            print(f"   {edge.tujuan:<8} {edge.jarak:<12} {status:<15}")
    else:
        print(f"   Tidak ada neighbors (node terisolasi)")
    
    input("\nTekan Enter untuk lanjut...")


def demo_delete_edge(system: EvacuationSystem) -> None:
    """Demo: DELETE - Menghapus Edge Secara Permanen"""
    print("\n" + "="*70)
    print("DEMO 5️⃣  OPERASI DELETE (REMOVE) - HAPUS EDGE SECARA PERMANEN")
    print("="*70)
    
    print("\n📊 STATUS GRAPH SEBELUM DELETE:")
    print(f"   Total edges: {system.graph.total_edges}")
    
    # Tanyakan edge yang akan dihapus
    print("\n📍 Pilih edge yang akan dihapus:")
    print(f"   Daftar node: {', '.join(sorted(system.graph.nodes.keys()))}")
    
    asal = input("\nNode asal (contoh: C): ").strip().upper()
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
    
    # Tampilkan info edge sebelum dihapus
    edge = next((e for e in system.graph.get_neighbors(asal) if e.tujuan == tujuan), None)
    
    print(f"\n📝 INFO EDGE SEBELUM DIHAPUS:")
    print(f"   Asal: {asal}")
    print(f"   Tujuan: {tujuan}")
    if edge:
        print(f"   Jarak: {edge.jarak} meter")
        print(f"   Status: {'✓ Aktif' if edge.is_active else '✗ Tertutup'}")
    
    print(f"\n📝 MENGHAPUS EDGE:")
    print(f"   Code: graph.remove_edge('{asal}', '{tujuan}')")
    print(f"   Operasi: BENAR-BENAR MENGHAPUS edge (tidak hanya marking)")
    print(f"   Catatan: Ini BEDA dengan close_edge() yang hanya marking!")
    
    # Hapus edge
    edges_before = system.graph.total_edges
    result = system.graph.remove_edge(asal, tujuan)
    
    if result:
        print(f"\n✅ HASIL SETELAH DELETE:")
        print(f"   Total edges: {edges_before} → {system.graph.total_edges}")
        print(f"   ✓ Edge BERHASIL dihapus secara PERMANEN!")
        print(f"   Neighbors {asal} sekarang: {[e.tujuan for e in system.graph.get_neighbors(asal)]}")
        print(f"   Neighbors {tujuan} sekarang: {[e.tujuan for e in system.graph.get_neighbors(tujuan)]}")
        print(f"\n   Catatan: Ini adalah OPERASI DELETE dalam struktur data.")
        print(f"   Data edge sudah dihapus dan TIDAK BISA dipulihkan.")
    else:
        print(f"❌ Edge tidak ditemukan!")
    
    input("\nTekan Enter untuk lanjut...")


def demo_delete_node(system: EvacuationSystem) -> None:
    """Demo: DELETE - Menghapus Node Beserta Edges-nya"""
    print("\n" + "="*70)
    print("DEMO 6️⃣  OPERASI DELETE (REMOVE) - HAPUS NODE + SEMUA KONEKSINYA")
    print("="*70)
    
    print("\n📊 STATUS GRAPH SEBELUM DELETE:")
    print(f"   Total nodes: {system.graph.total_nodes}")
    print(f"   Total edges: {system.graph.total_edges}")
    
    # Tanyakan node yang akan dihapus
    print("\n⚠️  PERINGATAN: Operasi ini akan menghapus node dan SEMUA edges-nya!")
    print("    Pilih node yang tidak penting untuk demo (tidak gunakan data utama).")
    
    print(f"\n📍 Daftar node: {', '.join(sorted(system.graph.nodes.keys()))}")
    node_id = input("\nMasukkan ID node untuk dihapus (contoh: Z): ").strip().upper()
    if node_id not in system.graph.nodes:
        print(f"❌ Node '{node_id}' tidak ditemukan!")
        return
    
    # Tampilkan info node sebelum dihapus
    neighbors_before = [e.tujuan for e in system.graph.get_neighbors(node_id)]
    node = system.graph.get_node(node_id)
    
    print(f"\n📝 INFO NODE SEBELUM DIHAPUS:")
    print(f"   {node.get_info()}")
    print(f"   Neighbors: {neighbors_before}")
    print(f"   Total koneksi: {len(neighbors_before)}")
    
    print(f"\n📝 MENGHAPUS NODE:")
    print(f"   Code: graph.remove_node('{node_id}')")
    print(f"   Operasi: Hapus node + SEMUA edges yang terhubung")
    print(f"   Proses:")
    print(f"   1. Identifikasi semua edges yang connect ke node ini")
    print(f"   2. Hapus node dari dictionary nodes")
    print(f"   3. Hapus node dari adjacency list")
    print(f"   4. Hapus semua edges dari nodes lain")
    
    # Hapus node
    nodes_before = system.graph.total_nodes
    edges_before = system.graph.total_edges
    result = system.graph.remove_node(node_id)
    
    if result:
        print(f"\n✅ HASIL SETELAH DELETE:")
        print(f"   Total nodes: {nodes_before} → {system.graph.total_nodes}")
        print(f"   Total edges: {edges_before} → {system.graph.total_edges}")
        print(f"   ✓ Node BERHASIL dihapus secara PERMANEN!")
        print(f"   ✓ Semua koneksi ke node juga TERHAPUS!")
        print(f"\n   Catatan: Ini adalah OPERASI DELETE dalam struktur data.")
        print(f"   Node dan semua relasinya sudah dihapus dan TIDAK BISA dipulihkan.")
    else:
        print(f"❌ Node tidak ditemukan!")
    
    input("\nTekan Enter untuk lanjut...")


def demo_close_vs_remove(system: EvacuationSystem) -> None:
    """Demo: Perbedaan close_edge (marking) vs remove_edge (delete)"""
    print("\n" + "="*70)
    print("DEMO 8️⃣  PERBEDAAN: close_edge() vs remove_edge()")
    print("="*70)
    
    print("\n📌 KONSEP PENTING - 2 OPERASI BERBEDA:")
    print("\n┌─ close_edge(asal, tujuan) ────────────────────────────────┐")
    print("│ • Menandai edge sebagai TIDAK AKTIF (is_active = False)   │")
    print("│ • Edge MASIH TERSIMPAN di graph                           │")
    print("│ • Total edges TIDAK BERUBAH                               │")
    print("│ • Bisa dibuka kembali dengan open_edge()                  │")
    print("│ • USE CASE: Simulasi kebakaran/jalur tertutup sementara  │")
    print("│ • BUKAN operasi DELETE yang sesungguhnya                  │")
    print("└────────────────────────────────────────────────────────────┘")
    
    print("\n┌─ remove_edge(asal, tujuan) ───────────────────────────────┐")
    print("│ • BENAR-BENAR MENGHAPUS edge dari graph                   │")
    print("│ • Edge TIDAK TERSIMPAN LAGI di graph                      │")
    print("│ • Total edges BERKURANG                                   │")
    print("│ • TIDAK bisa dikembalikan (permanent deletion)            │")
    print("│ • USE CASE: Maintenance/perbaikan permanen               │")
    print("│ • INI adalah operasi DELETE yang sesungguhnya            │")
    print("└────────────────────────────────────────────────────────────┘")
    
    print("\n" + "-"*70)
    print("DEMO PRAKTIKAL INTERAKTIF:")
    print("-"*70)
    
    # Pilih edge untuk demo
    print("\n📍 Pilih 2 edge untuk demonstrasi:")
    print(f"   Daftar node: {', '.join(sorted(system.graph.nodes.keys()))}")
    
    # Untuk demo close_edge
    print("\n📌 Edge 1 - Untuk demo close_edge():")
    asal1 = input("   Node asal (contoh: C): ").strip().upper()
    if asal1 not in system.graph.nodes:
        print(f"   ❌ Node '{asal1}' tidak ditemukan!")
        return
    
    neighbors1 = [e.tujuan for e in system.graph.get_neighbors(asal1)]
    if not neighbors1:
        print(f"   ❌ Node '{asal1}' tidak punya tetangga!")
        return
    
    print(f"   Tetangga {asal1}: {neighbors1}")
    tujuan1 = input("   Node tujuan: ").strip().upper()
    if tujuan1 not in neighbors1:
        print(f"   ❌ Tidak ada edge antara {asal1} dan {tujuan1}!")
        return
    
    # Untuk demo remove_edge
    print("\n📌 Edge 2 - Untuk demo remove_edge():")
    asal2 = input("   Node asal (contoh: D): ").strip().upper()
    if asal2 not in system.graph.nodes:
        print(f"   ❌ Node '{asal2}' tidak ditemukan!")
        return
    
    neighbors2 = [e.tujuan for e in system.graph.get_neighbors(asal2)]
    if not neighbors2:
        print(f"   ❌ Node '{asal2}' tidak punya tetangga!")
        return
    
    print(f"   Tetangga {asal2}: {neighbors2}")
    tujuan2 = input("   Node tujuan: ").strip().upper()
    if tujuan2 not in neighbors2:
        print(f"   ❌ Tidak ada edge antara {asal2} dan {tujuan2}!")
        return
    
    # ===== DEMO CLOSE_EDGE =====
    print("\n" + "="*70)
    print("STEP 1: DEMO close_edge() - HANYA MARKING (BUKAN DELETE)")
    print("="*70)
    
    print(f"\n📊 Sebelum close_edge('{asal1}', '{tujuan1}'):")
    print(f"   Total edges: {system.graph.total_edges}")
    edge1 = next((e for e in system.graph.get_neighbors(asal1) if e.tujuan == tujuan1), None)
    print(f"   Edge {asal1}→{tujuan1} aktif: {edge1.is_active if edge1 else 'N/A'}")
    
    print(f"\n📝 Memanggil: graph.close_edge('{asal1}', '{tujuan1}')")
    system.graph.close_edge(asal1, tujuan1)
    
    print(f"\n📊 Sesudah close_edge():")
    print(f"   Total edges: {system.graph.total_edges} ← TIDAK BERUBAH ✗")
    edge1 = next((e for e in system.graph.get_neighbors(asal1) if e.tujuan == tujuan1), None)
    print(f"   Edge {asal1}→{tujuan1} aktif: {edge1.is_active if edge1 else 'N/A'} ← Hanya marking")
    print(f"   ✓ Edge MASIH ADA di graph (hanya ditandai tidak aktif)")
    
    print(f"\n   Apa yang terjadi:")
    print(f"   - is_active = False (marking saja)")
    print(f"   - get_weight() return infinity (tidak bisa dilalui Dijkstra)")
    print(f"   - Tapi edge masih tersimpan di adjacency list")
    
    # ===== DEMO REMOVE_EDGE =====
    print("\n" + "="*70)
    print("STEP 2: DEMO remove_edge() - BENAR-BENAR DELETE")
    print("="*70)
    
    print(f"\n📊 Sebelum remove_edge('{asal2}', '{tujuan2}'):")
    print(f"   Total edges: {system.graph.total_edges}")
    neighbors2_before = [e.tujuan for e in system.graph.get_neighbors(asal2)]
    print(f"   Neighbors {asal2}: {neighbors2_before}")
    
    print(f"\n📝 Memanggil: graph.remove_edge('{asal2}', '{tujuan2}')")
    print(f"   Operasi: BENAR-BENAR HAPUS edge dari adjacency list")
    system.graph.remove_edge(asal2, tujuan2)
    
    print(f"\n📊 Sesudah remove_edge():")
    print(f"   Total edges: {system.graph.total_edges} ← BERKURANG 1 ✓")
    neighbors2_after = [e.tujuan for e in system.graph.get_neighbors(asal2)]
    print(f"   Neighbors {asal2}: {neighbors2_after} ← {tujuan2} hilang!")
    print(f"   ✓ Edge TIDAK ADA LAGI di graph (benar-benar dihapus)")
    
    print(f"\n   Apa yang terjadi:")
    print(f"   - Edge dihapus dari adjacency_list[{asal2}]")
    print(f"   - Edge dihapus dari adjacency_list[{tujuan2}]")
    print(f"   - total_edges berkurang")
    print(f"   - Tidak bisa dikembalikan")
    
    # ===== RINGKASAN =====
    print("\n" + "="*70)
    print("RINGKASAN PERBANDINGAN")
    print("="*70)
    print(f"\n{'Aspek':<20} {'close_edge()':<25} {'remove_edge()':<25}")
    print("-"*70)
    print(f"{'Menghapus data':<20} {'Tidak (hanya marking)':<25} {'Ya (permanen) ✓':<25}")
    print(f"{'Total edges berubah':<20} {'Tidak':<25} {'Ya ✓':<25}")
    print(f"{'Bisa dipulihkan':<20} {'Ya (open_edge)':<25} {'Tidak':<25}")
    print(f"{'Operasi DELETE':<20} {'Bukan':<25} {'Ya ✓':<25}")
    print(f"{'Struktur data':<20} {'Tetap utuh':<25} {'Berubah ✓':<25}")
    print("-"*70)
    
    print(f"\n✅ KESIMPULAN:")
    print(f"   • close_edge() = Simulasi saja (marking status)")
    print(f"   • remove_edge() = Operasi DELETE yang sesungguhnya")
    print(f"   • Untuk projek ini, close_edge() cocok untuk simulasi kebakaran")
    print(f"   • remove_edge() cocok untuk maintenance/perbaikan struktur graph")
    
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

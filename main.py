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
        print("5. Keluar")
        print("="*70)
        
        choice = input("\nPilih menu (1-5): ").strip()
        
        if choice == "1":
            system.run_interactive_mode()
        
        elif choice == "2":
            run_normal_scenarios(system)
        
        elif choice == "3":
            run_closed_path_scenarios(system)
        
        elif choice == "4":
            show_graph_info(system)
        
        elif choice == "5":
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

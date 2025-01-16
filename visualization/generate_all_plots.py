import os
from performance_analysis import analyze_network_performance
from time_efficiency import analyze_time_efficiency
from temporal_analysis import analyze_temporal_patterns
from topology_comparison import analyze_topology_impact
from load_analysis import analyze_network_load
from factor_analysis import analyze_key_factors
from rts_comparison import analyze_rts_impact

def ensure_plot_directory():
    os.makedirs('results/plots', exist_ok=True)

def generate_all_plots():
    ensure_plot_directory()
    
    print("Analyzing RTS/CTS impact...")
    analyze_rts_impact()
    
    print("Analyzing key factors...")
    analyze_key_factors()
    
    print("Analyzing network performance...")
    analyze_network_performance()
    
    print("Analyzing time efficiency...")
    analyze_time_efficiency()
    
    print("Analyzing temporal patterns...")
    analyze_temporal_patterns()
    
    print("Analyzing topology impact...")
    analyze_topology_impact()
    
    print("Analyzing network load...")
    analyze_network_load()
    
    print("All analyses completed successfully!")

if __name__ == "__main__":
    generate_all_plots() 
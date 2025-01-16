import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import load_all_results, parse_filename

def plot_throughput_comparison():
    results = load_all_results()
    
    plt.figure(figsize=(12, 6))
    for filename, df in results.items():
        params = parse_filename(filename)
        label = f"Stations: {params['station_count']}, Frame Rate: {params['frame_rate']}"
        plt.plot(df['current'], df['bps']/1e6, label=label, alpha=0.7)
    
    plt.xlabel('Time (ms)')
    plt.ylabel('Throughput (Mbps)')
    plt.title('Network Throughput Over Time')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('results/plots/throughput_comparison.png')
    plt.close()

if __name__ == "__main__":
    plot_throughput_comparison() 
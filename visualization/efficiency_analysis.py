import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from data_loader import load_all_results, parse_filename

def plot_network_efficiency():
    results = load_all_results()
    
    plt.figure(figsize=(12, 8))
    
    for filename, df in results.items():
        params = parse_filename(filename)
        # Calculate efficiency as ratio of actual to ideal processing
        efficiency = (df['processed'] / df['processed_ideal']) * 100
        label = f"Stations: {params['station_count']}, Frame Rate: {params['frame_rate']}"
        plt.plot(df['current'], efficiency, label=label, alpha=0.7)
    
    plt.xlabel('Time (ms)')
    plt.ylabel('Network Efficiency (%)')
    plt.title('Network Efficiency Over Time')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results/plots/efficiency_analysis.png')
    plt.close()

def plot_backoff_impact():
    results = load_all_results()
    
    stats_data = []
    for filename, df in results.items():
        params = parse_filename(filename)
        stats_data.append({
            'backoff_min': params['backoff_min'],
            'station_count': params['station_count'],
            'avg_throughput': df['bps'].mean() / 1e6,  # Convert to Mbps
            'efficiency': (df['processed'].mean() / df['processed_ideal'].mean()) * 100
        })
    
    stats_df = pd.DataFrame(stats_data)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    sns.boxplot(data=stats_df, x='backoff_min', y='avg_throughput', ax=ax1)
    ax1.set_title('Impact of Backoff on Throughput')
    ax1.set_xlabel('Minimum Backoff')
    ax1.set_ylabel('Average Throughput (Mbps)')
    
    sns.boxplot(data=stats_df, x='backoff_min', y='efficiency', ax=ax2)
    ax2.set_title('Impact of Backoff on Network Efficiency')
    ax2.set_xlabel('Minimum Backoff')
    ax2.set_ylabel('Efficiency (%)')
    
    plt.tight_layout()
    plt.savefig('results/plots/backoff_analysis.png')
    plt.close()

if __name__ == "__main__":
    plot_network_efficiency()
    plot_backoff_impact() 
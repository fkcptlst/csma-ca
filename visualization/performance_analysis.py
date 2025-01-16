import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from data_loader import load_all_results, parse_filename

def analyze_network_performance():
    """Analyze how primary control variables affect network performance"""
    results = load_all_results()
    
    # Prepare consolidated data
    performance_data = []
    for filename, df in results.items():
        params = parse_filename(filename)
        # Calculate average performance metrics for each configuration
        performance_data.append({
            'station_count': params['station_count'],
            'frame_rate': params['frame_rate'],
            'backoff_min': params['backoff_min'],
            'avg_throughput': df['bps'].mean(),
            'throughput_stability': df['bps'].std(),
            'utilization': (df['bps'] / df['max_bps']).mean() * 100,
            'collision_rate': df['collision_rate'].mean() * 100
        })
    
    perf_df = pd.DataFrame(performance_data)
    
    # Create visualization grid
    fig, axes = plt.subplots(2, 2, figsize=(15, 15))
    
    # Plot 1: Station Count vs Throughput
    sns.boxplot(data=perf_df, x='station_count', y='avg_throughput', 
                ax=axes[0,0])
    axes[0,0].set_title('Impact of Station Count on Throughput')
    axes[0,0].set_ylabel('Average Throughput (Kbps)')
    
    # Plot 2: Frame Rate vs Collision Rate
    sns.boxplot(data=perf_df, x='frame_rate', y='collision_rate',
                ax=axes[0,1])
    axes[0,1].set_title('Frame Rate vs Collision Rate')
    axes[0,1].set_ylabel('Collision Rate (%)')
    
    # Plot 3: Backoff vs Network Utilization
    sns.boxplot(data=perf_df, x='backoff_min', y='utilization',
                ax=axes[1,0])
    axes[1,0].set_title('Impact of Backoff on Network Utilization')
    axes[1,0].set_ylabel('Network Utilization (%)')
    
    # Plot 4: Station Count vs Throughput Stability
    sns.boxplot(data=perf_df, x='station_count', y='throughput_stability',
                ax=axes[1,1])
    axes[1,1].set_title('Impact on Throughput Stability')
    axes[1,1].set_ylabel('Throughput Standard Deviation')
    
    plt.tight_layout()
    plt.savefig('results/plots/network_performance.png')
    plt.close()

if __name__ == "__main__":
    analyze_network_performance() 
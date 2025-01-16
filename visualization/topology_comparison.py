import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from data_loader import load_all_results, parse_filename

def analyze_topology_impact():
    """Compare performance between star and non-star topologies"""
    results = load_all_results()
    
    # Prepare topology comparison data
    topology_data = []
    for filename, df in results.items():
        params = parse_filename(filename)
        topology_data.append({
            'station_count': params['station_count'],
            'frame_rate': params['frame_rate'],
            'star_topology': df['star_topology'].iloc[0],
            'with_rts': df['with_rts'].iloc[0],
            'avg_throughput': df['bps'].mean(),
            'collision_rate': df['collision_rate'].mean() * 100,
            'efficiency': (df['processed'] / df['processed_ideal']).mean() * 100
        })
    
    top_df = pd.DataFrame(topology_data)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 15))
    
    # Plot 1: Topology impact on throughput
    sns.boxplot(data=top_df, x='station_count', y='avg_throughput',
                hue='star_topology', ax=axes[0,0])
    axes[0,0].set_title('Topology Impact on Throughput')
    axes[0,0].set_ylabel('Average Throughput (Kbps)')
    
    # Plot 2: RTS/CTS effect
    sns.boxplot(data=top_df, x='station_count', y='collision_rate',
                hue='with_rts', ax=axes[0,1])
    axes[0,1].set_title('RTS/CTS Impact on Collision Rate')
    axes[0,1].set_ylabel('Collision Rate (%)')
    
    # Plot 3: Combined topology and RTS effect
    sns.boxplot(data=top_df[top_df['star_topology']], 
                x='station_count', y='efficiency',
                hue='with_rts', ax=axes[1,0])
    axes[1,0].set_title('Efficiency in Star Topology')
    axes[1,0].set_ylabel('Processing Efficiency (%)')
    
    # Plot 4: Non-star topology performance
    sns.boxplot(data=top_df[~top_df['star_topology']], 
                x='station_count', y='efficiency',
                hue='with_rts', ax=axes[1,1])
    axes[1,1].set_title('Efficiency in Non-Star Topology')
    axes[1,1].set_ylabel('Processing Efficiency (%)')
    
    plt.tight_layout()
    plt.savefig('results/plots/topology_comparison.png')
    plt.close()

if __name__ == "__main__":
    analyze_topology_impact() 
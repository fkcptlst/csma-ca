import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from data_loader import load_all_results, parse_filename

def plot_collision_statistics():
    results = load_all_results()
    
    # Prepare data for box plots
    stats_data = []
    for filename, df in results.items():
        params = parse_filename(filename)
        stats_data.append({
            'station_count': params['station_count'],
            'frame_rate': params['frame_rate'],
            'collision_rate': df['collision_rate'].mean(),
            'collisions': df['collisions'].sum()
        })
    
    stats_df = pd.DataFrame(stats_data)
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Collision rate vs station count
    sns.boxplot(data=stats_df, x='station_count', y='collision_rate', ax=ax1)
    ax1.set_title('Collision Rate vs Station Count')
    ax1.set_xlabel('Number of Stations')
    ax1.set_ylabel('Collision Rate')
    
    # Plot 2: Total collisions vs frame rate
    sns.boxplot(data=stats_df, x='frame_rate', y='collisions', ax=ax2)
    ax2.set_title('Total Collisions vs Frame Rate')
    ax2.set_xlabel('Frame Rate (fps)')
    ax2.set_ylabel('Total Collisions')
    
    plt.tight_layout()
    plt.savefig('results/plots/collision_analysis.png')
    plt.close()

if __name__ == "__main__":
    plot_collision_statistics() 
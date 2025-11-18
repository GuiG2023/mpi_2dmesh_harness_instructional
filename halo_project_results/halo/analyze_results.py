#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import math

def extract_timing_data():
   
    results_dir = '.'
    all_results = []
    
    for filename in os.listdir(results_dir):
        if filename.startswith('timing_') and filename.endswith('.log'):
            
            parts = filename.replace('timing_', '').replace('.log', '').split('_')
            decomp_name = parts[0]
            concurrency = int(parts[1].replace('procs', ''))
            
            with open(os.path.join(results_dir, filename), 'r') as f:
                content = f.read()
            
          
            scatter_match = re.search(r'Scatter time:\s+(\d+\.\d+)', content)
            sobel_match = re.search(r'Sobel time:\s+(\d+\.\d+)', content)
            gather_match = re.search(r'Gather time:\s+(\d+\.\d+)', content)
            
            if scatter_match and sobel_match and gather_match:
                all_results.append({
                    'concurrency': concurrency,
                    'decomposition': decomp_name,
                    'scatter_time_ms': float(scatter_match.group(1)),
                    'sobel_time_ms': float(sobel_match.group(1)),
                    'gather_time_ms': float(gather_match.group(1))
                })
    
    return pd.DataFrame(all_results)

def calculate_communication_metrics():
  
    IMAGE_WIDTH, IMAGE_HEIGHT = 7112, 5146
    CONCURRENCIES = [4, 9, 16, 25, 36, 49, 64, 81]
    FLOAT_SIZE = 4
    
    metrics = []
    for decomp_method, decomp_name in zip([1, 2, 3], ['row-slab', 'column-slab', 'tiled']):
        for concurrency in CONCURRENCIES:
            num_messages = 2 * (concurrency - 1)
            
            if decomp_method == 1:  # row-slab
                tile_width = IMAGE_WIDTH
                tile_height = IMAGE_HEIGHT // concurrency
            elif decomp_method == 2:  # column-slab
                tile_width = IMAGE_WIDTH // concurrency
                tile_height = IMAGE_HEIGHT
            else:  # tiled
                sqrt_conc = int(math.sqrt(concurrency))
                tile_width = IMAGE_WIDTH // sqrt_conc
                tile_height = IMAGE_HEIGHT // sqrt_conc
            
            tile_size_bytes = tile_width * tile_height * FLOAT_SIZE
            total_data_moved = tile_size_bytes * (concurrency - 1) * 2
            
            metrics.append({
                'concurrency': concurrency,
                'decomposition': decomp_name,
                'num_messages': num_messages,
                'total_data_moved_MB': total_data_moved / (1024 * 1024)
            })
    
    return pd.DataFrame(metrics)

def plot_speedup_charts(df):
   
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    decomp_methods = ['row-slab', 'column-slab', 'tiled']
    
    for idx, decomp in enumerate(decomp_methods):
        data = df[df['decomposition'] == decomp].sort_values('concurrency')
        
        if len(data) > 0:
            baseline = data[data['concurrency'] == 4]
            if len(baseline) > 0:
                base_scatter = baseline['scatter_time_ms'].iloc[0]
                base_sobel = baseline['sobel_time_ms'].iloc[0]
                base_gather = baseline['gather_time_ms'].iloc[0]
                
                scatter_speedup = base_scatter / data['scatter_time_ms']
                sobel_speedup = base_sobel / data['sobel_time_ms']
                gather_speedup = base_gather / data['gather_time_ms']
                
                axes[idx].plot(data['concurrency'], scatter_speedup, 'o-', label='Scatter', linewidth=2)
                axes[idx].plot(data['concurrency'], sobel_speedup, 's-', label='Sobel', linewidth=2)
                axes[idx].plot(data['concurrency'], gather_speedup, '^-', label='Gather', linewidth=2)
        
        axes[idx].set_xlabel('Concurrency')
        axes[idx].set_ylabel('Speedup')
        axes[idx].set_title(f'{decomp.title()} Decomposition')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
        axes[idx].set_ylim(bottom=0)
    
    plt.tight_layout()
    plt.savefig('./speedup_charts.png', dpi=300, bbox_inches='tight')
    print("✓ : speedup_charts.png")

def create_data_movement_table(comm_df):
  
    print("\n")
    print("Concurrency | Row-slab      | Column-slab   | Tiled")
    print("-" * 60)
    
    table_data = []
    for conc in [4, 9, 16, 25, 36, 49, 64, 81]:
        row_data = comm_df[(comm_df['concurrency'] == conc) & (comm_df['decomposition'] == 'row-slab')].iloc[0]
        col_data = comm_df[(comm_df['concurrency'] == conc) & (comm_df['decomposition'] == 'column-slab')].iloc[0]
        tile_data = comm_df[(comm_df['concurrency'] == conc) & (comm_df['decomposition'] == 'tiled')].iloc[0]
        
        print(f"{conc:11d} | {row_data['num_messages']:3d}/{row_data['total_data_moved_MB']:6.1f} MB | "
              f"{col_data['num_messages']:3d}/{col_data['total_data_moved_MB']:6.1f} MB | "
              f"{tile_data['num_messages']:3d}/{tile_data['total_data_moved_MB']:6.1f} MB")
        
        table_data.append({
            'concurrency': conc,
            'row_slab_msgs': row_data['num_messages'],
            'row_slab_data_MB': f"{row_data['total_data_moved_MB']:.1f}",
            'column_slab_msgs': col_data['num_messages'],
            'column_slab_data_MB': f"{col_data['total_data_moved_MB']:.1f}",
            'tiled_msgs': tile_data['num_messages'],
            'tiled_data_MB': f"{tile_data['total_data_moved_MB']:.1f}"
        })
    
    table_df = pd.DataFrame(table_data)
    table_df.to_csv('./data_movement_table.csv', index=False)
    print(f"\n✓ : data_movement_table.csv")

def main():
    print("=== CSC 746 CP#6 Halo  ===")
    
    
    timing_df = extract_timing_data()
    print(f"✓  {len(timing_df)} ")
    
    
    comm_df = calculate_communication_metrics()
    
  
    plot_speedup_charts(timing_df)
    
  
    create_data_movement_table(comm_df)
    
   
    timing_df.to_csv('./timing_analysis.csv', index=False)
    comm_df.to_csv('./communication_analysis.csv', index=False)
    print(f"✓ : timing_analysis.csv")
    print(f"✓ : communication_analysis.csv")
    
    print(f"\n=== files ===")
    print("- speedup_charts.png ")
    print("- data_movement_table.csv )")
    print("- timing_analysis.csv ")
    print("- communication_analysis.csv ")

if __name__ == "__main__":
    main()

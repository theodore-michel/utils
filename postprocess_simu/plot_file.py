import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import argparse
import os
import importlib.util

# Load plot style module
def load_style(name, location, stylename = "scientific_style"):
    spec = importlib.util.spec_from_file_location(name=name, location=location)
    if spec is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if stylename=="scientific_style":
            return module.scientific_style
        else: 
            print(f"Style {stylename} not found in module {name}.")
            return None
    else:
        print("Module specification is None. Check the file location.")
        return None
    
def main():
    # load style
    scientific_style = load_style("plot_styles", 
                                "C:/local/theodore.michel/9_GIT/utils/plot_styles.py", 
                                "scientific_style")
    plt.style.use(scientific_style)

    # Create argument parser
    parser = argparse.ArgumentParser(description='Plot file data')
    parser.add_argument('--file_path', type=str, help='Path to the input file')
    parser.add_argument('--additional_file_paths', nargs='*', type=str, help='Additional file paths to load and plot', default=[])
    args = parser.parse_args()

    # load data
    data            = pd.read_csv(args.file_path, sep='\t')
    additional_data = []
    simu_names      = [args.file_path.split("Resultats")[0].split("resultats")[0].split("/")[-2].strip() if "/" in args.file_path else args.file_path.split("Resultats")[0].split("resultats")[0].split("\\")[-2].strip()] # for plot legend
    if args.additional_file_paths:
        for path in args.additional_file_paths:
            additional_data.append(pd.read_csv(path, sep='\t'))
            name = path.split("Resultats")[0].split("resultats")[0].split("/")[-2].strip() if "/" in path else path.split("Resultats")[0].split("resultats")[0].split("\\")[-2].strip()
            simu_names.append(name)
    columns = list(data.columns)
    columns.remove('Temps')
    columns = [col for col in columns if data[col].notna().any()]
    if 'CompteurTemps' in columns:
        columns.remove('CompteurTemps')
    num_subplots = len(columns)

    # Plot
    fig = plt.figure(figsize=(10, 4*num_subplots))
    gs = gridspec.GridSpec(num_subplots, 2, figure=fig)
    for i, col in enumerate(columns):
        # define ax
        ax = fig.add_subplot(gs[i // 2, i % 2])
        ax.set_xlim(data['Temps'].iloc[0], data['Temps'].iloc[-1])
        total_temps  = len(data['Temps']) 
        start_index  = total_temps // 5 
        y_min, y_max = data[col][start_index:].min(), data[col][start_index:].max()
        ax.yaxis.set_ticks_position("both")
        ax.tick_params(axis='y', which='both', labelleft=True, labelright=True)
        # plot data
        ax.plot(data['Temps'], data[col], label=simu_names[0], linewidth=0.5)
        # plot cumulated avg
        if len(additional_data) == 0:
            start_cum = int(len(data['Temps']) / 4) # start cumulated avg after 25% of the simulation
            cum_avg   = data[col][start_cum:].expanding().mean()
            ax.plot(data['Temps'][start_cum:], cum_avg, label='cum avg', color='darkred', linewidth=2)
            ax.text(data['Temps'].iloc[-1], cum_avg.iloc[-1], f' {cum_avg.iloc[-1]:.2f}', color='darkred', ha='left', va='bottom', fontproperties=ax.yaxis.get_ticklabels()[0].get_fontproperties())
        # plot additional data
        else: 
            for j, additional_data_df in enumerate(additional_data):
                ax.plot(additional_data_df['Temps'], additional_data_df[col], label=simu_names[j+1], linewidth=0.5)
                y_min,y_max = min(y_min, additional_data_df[col][start_index:].min()), max(y_max, additional_data_df[col][start_index:].max())
        # settings
        ax.set_xlabel('Temps (s)')
        ax.set_ylabel(col)
        ylim_coeff = abs(y_max - y_min)*0.05 # 5% of the y-axis range in min and max margins
        ax.set_ylim(y_min-ylim_coeff, y_max+ylim_coeff) # update y-axis limits
        ax.grid(True)
        ax.legend(loc='upper right')

    # Adjust layout and save the plot
    file_name = os.path.basename(args.file_path)
    output_file_name = file_name.split("\\")[-1].split(".")[0] + "_plot.png"

    fig.suptitle("Simulation Outputs vs. Time")
    plt.tight_layout()
    plt.legend()
    plt.savefig(output_file_name)
    plt.show()

if __name__ == "__main__":
    main()
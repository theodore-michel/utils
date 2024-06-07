import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import argparse
import os
import json
import importlib.util
from jinja2 import Template


####################### INITILIZATION #######################
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

def get_simu_name(path):
    return path.split("Resultats")[0].split("resultats")[0].split("/")[-2].strip() if "/" in path else path.split("Resultats")[0].split("resultats")[0].split("\\")[-2].strip()

####################### LOAD DATA AND AUXILLARY FUNCTIONS #######################
def ABL(z):
    u_z = 42.5 * (z/274)**0.16
    return u_z

def Cp(p, z_ref, rho):
    q = 1/2 * rho * ABL(z_ref)**2
    return p / q

def format_template(template_path, replacement_dict):
    with open(template_path, 'r') as template_file:
        template_content  = template_file.read()
        template          = Template(template_content)
        formatted_content = template.render(replacement_dict)
        lines             = formatted_content.split('\n')
        GeometresModele   = '\n'.join(lines[0:8])
        ParametresModele  = '\n'.join(lines[9:19])
        DefGeoDistModele  = '\n'.join(lines[20:])
        return GeometresModele, ParametresModele, DefGeoDistModele
        

# format data
def format_data(directory, num_sensors):
    dataframes = []
    for i in range(1, num_sensors+1):
        filename = os.path.join(directory, f"Capteur{i}.txt")
        if os.path.isfile(filename):
            df = pd.read_csv(filename, sep='\t')
            df = df.dropna(axis=1, how='all')
            df = df.rename(columns={"Pression": f"Cp_{i}"})
            dataframes.append(df)
        else:
            print(f"File {filename} does not exist.")
    final_df = pd.concat(dataframes, axis=1)
    final_df = final_df.loc[:, ~final_df.columns.duplicated()]
    return(final_df)


##################### POSTPROCESSING #####################
def save_data(df, output_name, save=True, index=False):
    '''Save dataframe data'''
    if save:
        df.to_csv(f'{output_name}.csv', index=index)
    return(None)

def load_data(path):
    '''Load dataframe data'''
    return pd.read_csv(path)

def postprocess_data(df, num_sensors, z_ref, rho):
    '''Postprocess data to compute Cp and DeltaCp'''
    df.loc[:, 'Cp_1':f'Cp_{num_sensors}'] = df.loc[:, 'Cp_1':f'Cp_{num_sensors}'].apply(lambda col: col.apply(lambda x: Cp(x, z_ref, rho)) if col.name not in ['Temps', 'CompteurTemps'] else col, axis=0)
    for i in range(1, num_sensors//2+1):
        df[f"DeltaCp_{i}"] = df[f"Cp_{i}"] + df[f"Cp_{i+30}"] # aggregate of top and bottom surface coeffs by sensor pairs
    return(df)

def avg_postprocess_data(df, avg_time_coeff=2):
    '''Postprocess data to compute average Cp and DeltaCp'''
    last_time    = df['Temps'].iloc[-1]
    average_time = last_time / avg_time_coeff
    average_df   = df.copy()
    average_df   = average_df[average_df['Temps'] >= average_time]
    average_df   = average_df.mean(axis=0).to_frame().T
    average_df   = average_df.drop(['Temps', 'CompteurTemps'], axis=1)
    average_df   = average_df.T
    average_df.columns = ['avg_value'] + average_df.columns.tolist()[1:]
    return(average_df)

################### CREATE DICT OF SENSOR POSITION INFORMATION ###################
def create_capteur_dict(y_periods, x_periods, surfaces, num_sensors, coords_path='coords_capteurs.csv'):
    '''Create dictionnary of sensor positions'''
    sensor_dict = {} 
    index = 0
    coords_df = pd.read_csv(coords_path)
    # add dict entries
    for i in range(1, num_sensors+1):
        surface_index = (i-1) // int(num_sensors/len(surfaces)) % len(surfaces)
        y_index       = (i-1) // int(num_sensors/(len(y_periods)*len(surfaces))) % len(y_periods)
        x_index       = (i-1) // int(num_sensors/(len(x_periods)*len(y_periods)*len(surfaces))) % len(x_periods)
        capt_coords   = coords_df.iloc[i-1]
        sensor_dict[f"Capteur_{i}"] = {"y/L":y_periods[y_index], 
                                       "x/B":x_periods[x_index], 
                                       "surface":surfaces[surface_index],
                                       "coords":(round(capt_coords['x'],6), 
                                                 round(capt_coords['y'],6), 
                                                 round(capt_coords['z'],6))} # round for readability
    return(sensor_dict)

def save_dict(dict, save=False):
    '''Save sensor dict to json file'''
    if save:
        with open('sensor_dict.json', 'w') as json_file:
            json.dump(dict, json_file)
    return(None)

def get_capteur(y_p, x_p, surface, dict):
    '''Get sensor name from its relative position and surface side'''
    for key, value in dict.items():
        if value["y/L"] == y_p and value["x/B"] == x_p and value["surface"] == surface:
            return key
    return 'Position does not correspond to a sensor.'

def create_geometre_capteur(dict, template="template_Geometres.mtc", output="geometre_capteurs.mtc", which=[1]):
    '''Create geometre file for selected sensors to display in vtu as appartient etc.'''    
    sections = []
    # initial section sizes
    section1_start = 0 
    section2_start = 1
    section3_start = 2
    # write selected capteurs
    for i in which:
        geo_name=f"Capteur{i}"
        ls_name=f"Capteur{i}"
        type="Boule"
        origine=f"{dict[f'Capteur_{i}']['coords'][0]} {dict[f'Capteur_{i}']['coords'][1]} {dict[f'Capteur_{i}']['coords'][2]}"
        axes="1 0 0 0 1 0 0 0 1"
        rayon="0.0025"
        Forme = f"""
                    {{ Forme= 
                        {{ Type= Boule }}
                        {{ Dimension= 3 }}
                        {{ Data= 
                            {{ Rayon= {rayon} }} 
                        }}
                    }}
        """
        geo_params= {  "Dimension": "3",
                        "Origine": origine,
                        "Axes": axes,
                        "Coordonnees": "Coordonnees",
                        "PrecisionFrontiere": "PrecisionFrontieres",
                        "geo_name": geo_name,
                        "ls_name": ls_name,
                        "rayon":rayon,
                        "Forme": Forme
                    }
        GeometresModele, ParametresModele, DefGeoDistModele = format_template(template, geo_params)
        # group sections together
        sections.insert(section1_start, GeometresModele)
        sections.insert(section2_start, ParametresModele)
        sections.insert(section3_start, DefGeoDistModele)
        section1_start += 1
        section2_start += 2
        section3_start += 3
    with open(output, 'w') as file:
        file.write('\n'.join(sections))
    return(None)

################### PLOT CAPTEURS RESULTS ###################
# plot avg Cp
def plot_avg_cps(avg_df, dict, y_p_list, x_p_list, surface_list):
    '''Plot average Cp by sensor, selected according to their relative span and breadth positions and surface side'''
    num_subplots = len(y_p_list)
    num_cols = 2  # Number of columns in the grid
    num_rows = (num_subplots + num_cols - 1) // num_cols  # Number of rows in the grid
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 4*num_rows))
    axs = axs.flatten()  # Flatten the axs array to access each subplot
    ylims = []  # List to store the y-axis limits
    for i, y_p in enumerate(y_p_list):
        ax = axs[i] if num_subplots > 1 else axs
        for surface in surface_list:
            mrkr = 'o' if surface == 'upper' else '^'
            list_cp = []
            for x_p in x_p_list:
                capteur_name = get_capteur(y_p, x_p, surface, dict)
                if capteur_name:
                    list_cp.append(avg_df.loc[f'Cp_{capteur_name.split("_")[-1]}']['avg_value'])
            ax.plot(x_p_list, list_cp, linestyle='-', color='black', 
                    marker=mrkr, markersize=10, markerfacecolor='w', 
                    label=f'{surface} surface')
        ax.set_xlabel('$x/B$')
        ax.set_xlim(0, 1)
        ax.set_ylabel('$C_p$')
        ax.set_title(f'$y/L$={y_p}')
        ax.legend()
        ylims.extend(ax.get_ylim())  # Add the y-axis limits to the list
    ylim_min = min(ylims)  # Minimum y-axis limit
    ylim_max = max(ylims)  # Maximum y-axis limit
    for ax in axs:
        ax.set_ylim(ylim_min, ylim_max)  # Set the same y-axis limits for all subplots
    plt.suptitle(f'Average $C_p$ for $y/L$={y_p_list}')
    plt.tight_layout()
    plt.show()
    plt.close()

def compare_avg_cps(avg_df1, avg_df2, dict, y_p_list, x_p_list, surface_list, name1='1', name2='2'):
    '''Compare average Cp by sensor, selected according to their relative span and breadth positions and surface side'''
    num_subplots = len(y_p_list)
    num_cols = 2  # Number of columns in the grid
    num_rows = (num_subplots + num_cols - 1) // num_cols  # Number of rows in the grid
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 4*num_rows))
    axs = axs.flatten()  # Flatten the axs array to access each subplot
    ylims = []  # List to store the y-axis limits
    for i, y_p in enumerate(y_p_list):
        ax = axs[i] if num_subplots > 1 else axs
        for surface in surface_list:
            mrkr = 'o' if surface == 'upper' else '^'
            list_cp1 = []
            list_cp2 = []
            for x_p in x_p_list:
                capteur_name = get_capteur(y_p, x_p, surface, dict)
                if capteur_name:
                    list_cp1.append(avg_df1.loc[f'Cp_{capteur_name.split("_")[-1]}']['avg_value'])
                    list_cp2.append(avg_df2.loc[f'Cp_{capteur_name.split("_")[-1]}']['avg_value'])
            ax.plot(x_p_list, list_cp1, linestyle='-', color='black', 
                    marker=mrkr, markersize=10, markerfacecolor='w', 
                    label=f'{surface} surf {name1}')
            ax.plot(x_p_list, list_cp2, linestyle='--', color='darkred', 
                    marker=mrkr, markersize=10, markerfacecolor='w', 
                    label=f'{surface} surf {name2}')
        ax.set_xlabel('$x/B$')
        ax.set_xlim(0, 1)
        ax.set_ylabel('$C_p$')
        ax.set_title(f'$y/L$={y_p}')
        ax.legend()
        ylims.extend(ax.get_ylim())  # Add the y-axis limits to the list
    ylim_min = min(ylims)  # Minimum y-axis limit
    ylim_max = max(ylims)  # Maximum y-axis limit
    for ax in axs:
        ax.set_ylim(ylim_min, ylim_max)  # Set the same y-axis limits for all sub
    plt.suptitle(f'Comparing avg $C_p$ for $y/L$={y_p_list} -- {name1} vs. {name2}')
    plt.tight_layout()
    plt.show()
    plt.close()

# plot Cp 
def plot_cps(df, columns):
    '''Plot Cp vs Time, selected by Cp name list in columns'''
    colors = plt.cm.coolwarm
    fig = plt.figure(figsize=(10, 6))
    for i, column in enumerate(columns[1:]):
        plt.plot(df['Temps'], df[column], label=column, color=colors(i / (len(columns) - 1)))
    yaxisname = columns[1].split('_')[0]
    xaxisname = columns[0].split('_')[0]
    plt.title(f'{yaxisname} vs {xaxisname}')
    plt.xlabel(xaxisname)
    plt.ylabel(yaxisname)
    plt.legend()
    plt.show()
    plt.close()



################### EXECUTE ###################

def main():
    ### load style
    scientific_style = load_style("plot_styles", 
                                "C:/local/theodore.michel/9_GIT/utils/plot_styles.py", 
                                "scientific_style")
    plt.style.use(scientific_style)

    ### create argument parser
    parser = argparse.ArgumentParser(description='Get directory of sensor files and number of sensors')
    parser.add_argument('--directory',      type=str,   help='Directory of sensor files')
    parser.add_argument('--num_sensors',    type=int,   help='Number of sensors')
    parser.add_argument('--coords',         type=str,   default='coords_capteurs.csv', help='file path of coordinates of sensors')
    parser.add_argument('--save',           type=bool,  default=True, help='Save the postprocessed data')
    parser.add_argument('--create_geo',     type=bool,  default=False, help='Create geometre.mtc file for selected sensors')
    parser.add_argument('--template_path',  type=str,   default="./template_Geometre.mtc", help='Path to the template mtc file for geometres.mtc creation')
    parser.add_argument('--add_cp_data',    type=str,   help='additional avg Cp data filepath to compare with')
    args = parser.parse_args()

    ### parser data
    directory   = args.directory
    num_sensors = args.num_sensors
    coords_path = args.coords
    save_post   = args.save
    create_geo  = args.create_geo
    template    = args.template_path
    add_cp_data = args.add_cp_data
    
    ### case-specific parameters
    Z_REF     = 0.6     # lowest point of the inclined model's surface
    RHO       = 1.225   # air density 
    y_periods = [-0.99, -0.67, -0.01, 0.01, 0.67, 0.99]     # y_period = y/(panel_span/2) coord from center of panel
    x_periods = [0.01, 0.21, 0.45, 0.78, 0.95]              # x_period = (x and z)/panel_breadth coords from center of panel
    surfaces  = ['upper', 'lower']                          # surface of the panel

    ### postprocess capteurs data
    final_df = format_data(directory=directory, 
                           num_sensors=num_sensors)
    final_df = postprocess_data(df=final_df, 
                                num_sensors=num_sensors, 
                                z_ref=Z_REF, 
                                rho=RHO)
    average_df = avg_postprocess_data(df=final_df, 
                                      avg_time_coeff=2)
    save_data(df=final_df, 
              output_name='postprocessed_capteurs', 
              save=save_post,
              index=False)
    save_data(df=average_df, 
              output_name='average_capteurs', 
              save=save_post,
              index=True)

    ### group sensor data for plotting
    sensor_dict = create_capteur_dict(y_periods=y_periods, 
                                      x_periods=x_periods, 
                                      surfaces=surfaces, 
                                      num_sensors=num_sensors, 
                                      coords_path=coords_path)
    save_dict(dict=sensor_dict, 
              save=save_post)

    ### create geometre file for selected sensors
    if create_geo:
        create_geometre_capteur(dict=sensor_dict, 
                                template=template,
                                output="./geometre_capteurs.mtc", 
                                which=[1,2,3]) 
                                # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
    
    ### plot 
    # selected_columns1 = ['Temps', 'Cp_1', 'Cp_6', 'Cp_11', 'Cp_16', 'Cp_21', 'Cp_26']
    # plot_cps(final_df[selected_columns1], selected_columns1)
    plot_avg_cps(avg_df=average_df, 
                 dict=sensor_dict,
                 y_p_list=y_periods, 
                 x_p_list=x_periods, 
                 surface_list=surfaces)
    if add_cp_data:
        additional_cp_data = load_data(add_cp_data)
        simu_name_1 = get_simu_name(directory)
        simu_name_2 = get_simu_name(add_cp_data)
        compare_avg_cps(avg_df1=average_df, 
                        avg_df2=additional_cp_data, 
                        name1=simu_name_1,
                        name2=simu_name_2,
                        dict=sensor_dict,
                        y_p_list=y_periods, 
                        x_p_list=x_periods, 
                        surface_list=surfaces)

    
if __name__ == "__main__":
    main()
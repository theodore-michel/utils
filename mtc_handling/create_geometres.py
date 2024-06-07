import argparse
import json
import os
from jinja2 import Template

# Create argument parser
parser = argparse.ArgumentParser(description='Create mtc geometres')
parser.add_argument('--geo_name',   type=str,                                   help='Geometre name')
parser.add_argument('--ls_name',    type=str,                                   help='Appartient and LevelSet name')
parser.add_argument('--type',       type=str,                                   help='Geometre type: Maillage, DemiPlan, Boule')
parser.add_argument('--template',   type=str, default="template_Geometre.mtc",  help='Geoemetre template file path')
parser.add_argument('--origine',    type=str, default="0 0 0",                  help='Geometre origin')
parser.add_argument('--axes',       type=str, default="1 0 0 0 1 0 0 0 1",      help='Geometre axes')
parser.add_argument('--rayon',      type=str, default="0.1",                    help='Rayon of Boule if geo type is Boule')
args = parser.parse_args()

# parse data
geo_name = args.geo_name
ls_name  = args.ls_name
type     = args.type
template = args.template
origine  = args.origine
axes     = args.axes


### Create Geometre

def format_template(template_path, output_path, replacement_dict):
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
    template = Template(template_content)
    formatted_content = template.render(replacement_dict)
    with open(output_path, 'w') as output_file:
        output_file.write(formatted_content)

# geometre data
geo_params= {  "Dimension": "3",
                "Origine": origine,
                "Axes": axes,
                "Coordonnees": "Coordonnees",
                "PrecisionFrontiere": "PrecisionFrontiere",
                "geo_name": geo_name,
                "ls_name": ls_name
            }

if type == "Maillage":
    Forme = f"""
                {{ Forme = 
                    {{ Type = FormNewMaillageBis }}
                    {{ Data =
                        {{ M: {geo_name}.t }}
                        {{ Localisation=
                            {{ Brique= Boite }}
                            {{ Methode= Lineaire }}
                            {{ TailleMax = 1024 }}
                        }}
                    }}
                }}
    """
elif type == "DemiPlan":
    Forme = f"""
                {{ Forme=
                    {{ Type= DemiPlan }}
                    {{ Dimension= 2 }}
                }}
    """
elif type == "Boule":
    Forme = f"""
                {{ Forme= 
                    {{ Type= Boule }}
                    {{ Dimension= 3 }}
                    {{ Data= 
                        {{ Rayon= 0.1 }} 
                    }}
                }}
    """
geo_params["Forme"] = Forme

format_template(template, f"{geo_name}_Geometre.mtc", geo_params)
    

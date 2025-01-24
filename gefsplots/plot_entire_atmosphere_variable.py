#!/usr/bin/env python
"""
GEFS Surface Variable Plotting Tool

This module provides functionality to plot surface variables from the GEFS model.
It can access GEFS data from AWS S3 and create visualizations with customizable parameters.

Available variables:
 - bcAOD550 : Black Carbon Aerosol Optical Depth at 550 nm
 - bcScatAOD550 : Black Carbon Aerosol Scattering Aerosol Optical Depth at 550 nm
 - bc_pm236_colmd : Black Carbon Aerosol Column Mass Density at 236 nm
 - duAOD550 : Dust Aerosol Optical Depth at 550 nm
 - duScatAOD550 : Dust Aerosol Scattering Aerosol Optical Depth at 550 nm
 - du_pm25_colmd : Dust Aerosol Column Mass Density at 236 nm
 - omAOD550 : Organic Matter Aerosol Optical Depth at 550 nm 
 - omScatAOD550 : Organic Matter Aerosol Scattering Aerosol Optical Depth at 550 nm
 - om_pm424_colmd : Organic Matter Aerosol Column Mass Density at 424 nm
 - so4AOD550 : Sulfate Aerosol Optical Depth at 550 nm
 - so4ScatAOD550 : Sulfate Aerosol Scattering Aerosol Optical Depth at 550 nm 
 - so4_pm25_colmd : Sulfate Aerosol Column Mass Density at 236 nm
 - ssAOD550 : Sea Salt Aerosol Optical Depth at 550 nm
 - ssScatAOD550 : Sea Salt Aerosol Scattering Aerosol Optical Depth at 550 nm
 - ss_pm25_colmd : Sea Salt Aerosol Column Mass Density at 236 nm
 - totAOD11100 : Total Aerosol Optical Depth at 11100 nm 
 - totAOD1640 : Total Aerosol Optical Depth at 1640 nm
 - totAOD340 : Total Aerosol Optical Depth at 340 nm
 - totAOD440 : Total Aerosol Optical Depth at 440 nm
 - totAOD550 : Total Aerosol Optical Depth at 550 nm
 - totAOD645 : Total Aerosol Optical Depth at 645 nm
 - totAOD870 : Total Aerosol Optical Depth at 870 nm
 - totAsy340 : Total Aerosol Asymmetry Parameter at 340 nm
 - totSSA340 : Total Single Scattering Albedo at 340 nm
 - totScatAOD550 : Total Scattering Aerosol Optical Depth at 550 nm
 - tot_pm10_colmd : Total Aerosol Column Mass Density for pm10
 - tot_pm25_colmd : Total Aerosol Column Mass Density for pm2.5

"""

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import fsspec
import monet
import argparse
from datetime import datetime

def parse_arguments():
    """
    Parse command line arguments for the GEFS plotting script.

    Returns:
        argparse.Namespace: Parsed command line arguments containing:
            - date: Date string in MM-DD-YYYY format
            - cycle: Forecast cycle (00, 06, 12, 18)
            - variable: Variable name to plot
            - levels: List of contour levels
            - output: Output filename
    """
    parser = argparse.ArgumentParser(description='Plot GEFS surface data')
    parser.add_argument('--date', type=str, help='Date in MM-DD-YYYY format', default='01-22-2025')
    parser.add_argument('--cycle', type=str, choices=['00', '06', '12', '18'], default='12',
                        help='Forecast cycle (00, 06, 12, 18)')
    parser.add_argument('--variable', type=str, default='totAOD550',
                        help='Variable to plot from GEFS')
    parser.add_argument('--levels', type=float, nargs='+',
                        default=[1, 2, 4, 8, 16, 32, 64, 128],
                        help='Contour levels for plotting')
    parser.add_argument('--output', type=str, default='gefs_plot.jpg',
                        help='Output filename')
    return parser.parse_args()

def get_gefs_data(date_str, cycle, variable):
    """
    Retrieve GEFS data from AWS S3 for specified parameters.

    Args:
        date_str (str): Date string in MM-DD-YYYY format
        cycle (str): Forecast cycle (00, 06, 12, 18)
        variable (str): Variable name to retrieve

    Returns:
        xarray.Dataset: Dataset containing the requested GEFS data
    """
    d = pd.Timestamp(date_str)
    yyyymmdd = d.strftime('%Y%m%d')
    base_url = f"simplecache::s3://noaa-gefs-pds/gefs.{yyyymmdd}/{cycle}/chem/pgrb2ap25/gefs.chem.t{cycle}z.a2d_0p25.f018.grib2"
    file = fsspec.open_local(base_url, s3={'anon':True}, filecache={'cache_storage':'/tmp/files'})
    filters = dict(typeOfFirstFixedSurface=10, productDefinitionTemplateNumber=48)
    return xr.open_dataset(file, engine='grib2io', filters=filters)

def create_plot(ds, variable, levels, output_file):
    """
    Create and save a plot of the specified GEFS variable.

    Args:
        ds (xarray.Dataset): Dataset containing GEFS data
        variable (str): Variable name to plot
        levels (list): Contour levels for plotting
        output_file (str): Path to save the output plot

    Returns:
        None
    """
    cmap = plt.get_cmap('turbo')
    cmap.set_extremes(under='white')
    
    ax = ds[variable].monet.quick_imshow(
        cmap=cmap,
        roll_dateline=True,
        levels=levels,
        map_kws={'states':True},
        figsize=(10,10)
    )
    
    ax.set_ylim([10,50])
    ax.set_xlim([-130,-90])
    monet.savefig(output_file)
    plt.show()

def main():
    """
    Main execution function that orchestrates the GEFS data retrieval and plotting process.
    Parses command line arguments, retrieves data, and creates the visualization.
    """
    args = parse_arguments()
    ds = get_gefs_data(args.date, args.cycle, args.variable)
    create_plot(ds, args.variable, args.levels, args.output)

if __name__ == '__main__':
    main()

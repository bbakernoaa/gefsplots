#!/usr/bin/env python
"""
GEFS Surface Variable Plotting Tool

This module provides functionality to plot surface variables from the GEFS model.
It can access GEFS data from AWS S3 and create visualizations with customizable parameters.

This pulls the GEFS 0.5 degree data from the AWS S3 bucket and plots the specified variable.
Available variables:
 - bchi_pm236 : bc hydrophilic aerosol pm 0.236
 - bcho_pm236 : bc hydrophobic aerosol pm 0.236
 - du_pm120   : dust aerosol pm 0.120
 - du_pm2     : dust aerosol pm 2
 - du_pm20    : dust aerosol pm 0.2
 - du_pm36    : dust aerosol pm 3.6
 - du_pm60    : dust aerosol pm 6.0
 - omhi_pm424 : organic matter hydrophilic aerosol pm 0.424
 - omho_pm424 : organic matter hydrophobic aerosol pm 0.424
 - so4_pm139  : sulfate aerosol pm 0.139
 - ss_pm10    : sea salt aerosol pm 10
 - ss_pm100   : sea salt aerosol pm 0.1
 - ss_pm2     : sea salt aerosol pm 2
 - ss_pm30    : sea salt aerosol pm 0.3
 - ss_pm6     : sea salt aerosol pm 6
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
    parser.add_argument('--variable', type=str, default='sfc_tot_pm25',
                        help='Variable to plot from GEFS')
    parser.add_argument('--levels', type=float, nargs='+',
                        default=[1, 2, 4, 8, 16, 32, 64, 128],
                        help='Contour levels for plotting')
    parser.add_argument('--output', type=str, default='gefs_plot.jpg',
                        help='Output filename')
    parser.add_argument('--model_level', type=int, default=1)
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
    base_url = f"simplecache::s3://noaa-gefs-pds/gefs.{yyyymmdd}/{cycle}/chem/pgrb2ap5/gefs.chem.t{cycle}z.a3d_0p25.f018.grib2"
    file = fsspec.open_local(base_url, s3={'anon':True}, filecache={'cache_storage':'/tmp/files'})
    return xr.open_dataset(file, engine='grib2io')

def create_plot(ds, variable, model_level, levels, output_file):
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
    
    ax = ds[variable].sel(valueOfFirstFixedSurface=model_level).monet.quick_imshow(
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
    create_plot(ds, args.variable, args.model_level, args.levels, args.output)

if __name__ == '__main__':
    main()

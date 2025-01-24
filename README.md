# gefsplots

Python tools for plotting GEFS (Global Ensemble Forecast System) aerosol and chemistry forecasts from AWS S3.

## Installation

There are two ways to install gefsplots:

### 1. Using pip with requirements.txt (recommended)
```bash
git clone https://github.com/YourUsername/gefsplots.git
cd gefsplots
pip install -r requirements.txt
pip install -e .
```

### 2. Using setup.py directly
```bash
git clone https://github.com/YourUsername/gefsplots.git
cd gefsplots
pip install -e .
```

Note: If you experience issues with grib2io installation, you can install it separately:
```bash
pip install git+https://github.com/noaa-mdl/grib2io.git
```

## Usage Examples

### 1. Plot Surface Variables

```bash
# Plot surface PM2.5 with default settings
python gefsplots/plot_sfc_variable.py

# Plot surface PM2.5 for a specific date and forecast cycle
python gefsplots/plot_sfc_variable.py --date "01-23-2025" --cycle "00" --variable "sfc_tot_pm25"

# Customize contour levels and output filename
python gefsplots/plot_sfc_variable.py --levels 1 5 10 15 20 25 30 35 --output "pm25_forecast.jpg"
```

### 2. Plot Column-Integrated Variables

```bash
# Plot total AOD at 550nm
python gefsplots/plot_entire_atmosphere_variable.py --variable "totAOD550"

# Plot black carbon AOD with custom levels
python gefsplots/plot_entire_atmosphere_variable.py --variable "bcAOD550" --levels 0.01 0.02 0.05 0.1 0.2 0.5
```

### 3. Plot Half-Degree Resolution Data

```bash
# Plot dust PM2.5
python gefsplots/plot_halfdegree_dta.py --variable "du_pm2"
```

## Available Variables

### Surface Variables
- `sfc_du_pm10`: Surface Dust PM10 Concentration
- `sfc_du_pm25`: Surface Dust PM2.5 Concentration
- `sfc_ss_pm25`: Surface Sea Salt PM2.5 Concentration
- `sfc_tot_pm10`: Surface Total PM10 Concentration
- `sfc_tot_pm25`: Surface Total PM2.5 Concentration

### Column-Integrated Variables
- `totAOD550`: Total Aerosol Optical Depth at 550nm
- `bcAOD550`: Black Carbon AOD at 550nm
- `duAOD550`: Dust AOD at 550nm
- `ssAOD550`: Sea Salt AOD at 550nm
- `so4AOD550`: Sulfate AOD at 550nm
- (See script docstring for full list)

### Half-Degree Resolution Variables
- `du_pm2`: Dust aerosol PM2.5
- `ss_pm2`: Sea salt aerosol PM2.5
- `bchi_pm236`: BC hydrophilic aerosol
- `omhi_pm424`: Organic matter hydrophilic aerosol
- (See script docstring for full list)

## Command Line Arguments

All scripts support the following arguments:
- `--date`: Forecast date in MM-DD-YYYY format (default: current date)
- `--cycle`: Forecast cycle (00/06/12/18, default: 12)
- `--variable`: Variable name to plot
- `--levels`: Custom contour levels
- `--output`: Output filename

## Dependencies

- xarray
- matplotlib
- pandas
- fsspec
- monet
- grib2io
- cartopy (for mapping)
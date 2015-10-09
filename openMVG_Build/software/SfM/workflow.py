#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# A simple workflow for OpenMVG based on the openMVG tutorial v.0.1

import commands
import os
import subprocess
import sys

# Define global vars

def get_parent_dir(directory):
    import os
    return os.path.dirname(directory)

# Define which vars are going to be used by the script
allstrings = ['inputpath', 'image1', 'image2', 'export_cmpmvs', 'export_pmvs'];

# Variablen initialisieren
index_argv = 1;
index_allstrings = 0;
index_user_vars = 0;
user_vars = {allstrings[0]: 'ERROR'};
total_output = "Workflow beendet.";

# Durchlauf um Strings aus allstrings auszulesen und in dictionary user_vars mit den keys aus sys.argv zu speichern
for num in sys.argv[1:]:
 index_allstrings = 0;
 for num2 in allstrings[0:]:
  if sys.argv[index_argv].find(allstrings[index_allstrings]):
   pass
  else:
   user_vars[allstrings[index_allstrings]] = sys.argv[index_argv];
   index_user_vars = index_user_vars+1;
  index_allstrings = index_allstrings+1;
 index_argv = index_argv+1;

# Arrays vorbereiten um Inhalte auszulesen
index_allstrings = 0;
for num in user_vars:
 user_vars[allstrings[index_allstrings]] = user_vars[allstrings[index_allstrings]].replace(allstrings[index_allstrings] + "=", "")
 index_allstrings = index_allstrings+1;

# !!! HIER DIE VARIABLEN ÄNDERN !!! 

arbeitsverzeichnis = user_vars["inputpath"]
image1 = user_vars["image1"]
image2 = user_vars["image2"]
export_pmvs = user_vars["export_pmvs"]
export_cmpmvs = user_vars["export_cmpmvs"]

# !!! ENDE DER VARIABLEN !!! 

# Indicate the openMVG binary directory
OPENMVG_SFM_BIN = os.path.dirname(os.path.abspath(__file__))
# Indicate the openMVG camera sensor width directory
CAMERA_SENSOR_WIDTH_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + "/cameraSensorWidth"
# Indicate Input dir
input_eval_dir = arbeitsverzeichnis
# Check if last character is a / and if so cut output dir by 1 and appemd _out
if arbeitsverzeichnis.endswith('/'): output_eval_dir = os.path.join(arbeitsverzeichnis[:-1] + "_out")
else: output_eval_dir = os.path.join(arbeitsverzeichnis + "_out")

if not os.path.exists(output_eval_dir):
  os.mkdir(output_eval_dir)

input_dir = input_eval_dir
output_dir = output_eval_dir
print ("Using input dir  : ", input_dir)
print ("      output_dir : ", output_dir)
    
matches_dir = os.path.join(output_dir, "matches")
camera_file_params = os.path.join(CAMERA_SENSOR_WIDTH_DIRECTORY, "cameraGenerated.txt")

# Create the ouput/matches folder if not present
if not os.path.exists(matches_dir):
  os.mkdir(matches_dir)

# -c = 3 = default pinhole camera
print ("1. Image listing - generate sfm_data.json") 
pIntrisics = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),  "-i", input_dir, "-o", matches_dir, "-d", camera_file_params, "-c", "3"] )
pIntrisics.wait()

print ("2. Compute features")
pFeatures = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-m", "SIFT", "-f" , "1"] )
pFeatures.wait()

# -r = ratio (0.8 is recommended) -f = force to recompute data every time
print ("3.1 SEQUENTIAL: Compute matches")
pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-r", "0.8", "-f", "1"] )
pMatches.wait()

#set manually the initial pair to avoid the prompt question
reconstruction_dir = os.path.join(output_dir,"reconstruction_sequential")
print ("3.2 SEQUENTIAL: Reconstruction") 
print ("You selected", image1, "and", image2, "as matches")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_IncrementalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir, "-a", image1, "-b", image2] )
pRecons.wait()

print ("3.3 SEQUENTIAL: Colorize Structure")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/sfm_data.json", "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
pRecons.wait()

print ("3.4 SEQUENTIAL: Structure from Known Poses (robust triangulation)")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.json", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
pRecons.wait()

# Check if export bools are false, if not export to PMVS and CMPMVS

if export_pmvs == "false":
 pass
else:
 print ("3.5. Export Sequential results to PMVS")
 pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2PMVS"),  "-i", reconstruction_dir+"/sfm_data.json", "-o", reconstruction_dir] )
 total_output += ("The sequential PMVS folder was created in the "+reconstruction_dir+"/PMVS directory")
 pRecons.wait()

if export_cmpmvs == "false":
 pass
else:
 print ("3.6. Export Sequential results to CMPMVS")
 pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2CMPMVS"),  "-i", reconstruction_dir+"/sfm_data.json", "-o", reconstruction_dir] )
 total_output += ("The sequential CMPMVS folder was created in the "+reconstruction_dir+"/CMPMVS directory")
 pRecons.wait()

# Reconstruction for the global SfM pipeline
# - global SfM pipeline use matches filtered by the essential matrices
# - g; f: Fundamental matrix filtering e: Essential matrix filtering (all the image must have the same known focal length) h: Homography matrix filtering

print ("4.1 GLOBAL: Compute matches")
pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-r", "0.8", "-g", "e"] )
pMatches.wait()

# Reconstruction dir wechseln
reconstruction_dir = os.path.join(output_dir,"reconstruction_global")

print ("4.2 GLOBAL: Reconstruction")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_GlobalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir] )
pRecons.wait()

print ("4.3 GLOBAL: Colorize Structure")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/sfm_data.json", "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
pRecons.wait()

print ("4.4 GLOBAL: Structure from Known Poses (robust triangulation)")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.json", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
pRecons.wait()

# Check if export bools are false, if not export to PMVS and CMPMVS

if export_pmvs == "false":
 pass
else:
 print ("4.5 Export global results to PMVS")
 pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2PMVS"),  "-i", reconstruction_dir+"/sfm_data.json", "-o", reconstruction_dir] )
 total_output += ("The global PMVS folder was created in the "+reconstruction_dir+"/PMVS directory")
 pRecons.wait()

if export_cmpmvs == "false":
 pass
else:
 print ("4.6. Export global results to CMPMVS")
 pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2CMPMVS"),  "-i", reconstruction_dir+"/sfm_data.json", "-o", reconstruction_dir] )
 total_output += ("The global CMPMVS folder was created in the "+reconstruction_dir+"/PMVS directory")
 pRecons.wait()

print total_output

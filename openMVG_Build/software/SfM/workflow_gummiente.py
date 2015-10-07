#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# A simple workflow for OpenMVG based on the openMVG tutorial

# Indicate the openMVG binary directory
# OPENMVG_SFM_BIN = "/home/martin/openMVG_Build/software/SfM"

# Indicate the openMVG camera sensor width directory
# CAMERA_SENSOR_WIDTH_DIRECTORY = "/home/martin/openMVG/src/software/SfM" + "/cameraSensorWidth"

import commands
import os
import subprocess
import sys

def get_parent_dir(directory):
    import os
    return os.path.dirname(directory)

# !!! HIER DIE VARIABLEN ÄNDERN !!! 

arbeitsverzeichnis = "/gummiente"
image1 = "_MG_4800.JPG"
image2 = "_MG_4801.JPG"

# !!! ENDE DER VARIABLEN !!! 

# Indicate the openMVG binary directory
OPENMVG_SFM_BIN = os.path.dirname(os.path.abspath(__file__))
# Indicate the openMVG camera sensor width directory
CAMERA_SENSOR_WIDTH_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + "/cameraSensorWidth"
# Indicate Input dir
input_eval_dir = os.path.dirname(os.path.abspath(__file__)) + arbeitsverzeichnis
# Indicate Output dir
output_eval_dir = os.path.join(get_parent_dir(input_eval_dir) + arbeitsverzeichnis + "_out")

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

# -c = default pinhole camera
print ("1. Image listing - generate sfm_data.json") 
pIntrisics = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),  "-i", input_dir, "-o", matches_dir, "-d", camera_file_params, "-c", "3"] )
pIntrisics.wait()

print ("2. Compute features")
pFeatures = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-m", "SIFT", "-f" , "1"] )
pFeatures.wait()

# -r = ratio (0.8 is recommended) -f = force to recompute data
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

print ("3.5. Export to PMVS")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2PMVS"),  "-i", reconstruction_dir+"/sfm_data.json", "-o", reconstruction_dir] )
print ("Der PMVS Ordner wurde aus der Datei "+reconstruction_dir+"/sfm_data.json in das Verzeichnis "+reconstruction_dir+" erstellt")
pRecons.wait()

print ("3.6. Export to CMPMVS")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2CMPMVS"),  "-i", reconstruction_dir+"/sfm_data.json", "-o", reconstruction_dir] )
print ("Der CMPMVS Ordner wurde aus der Datei "+reconstruction_dir+"/sfm_data.json in das Verzeichnis "+reconstruction_dir+" erstellt")
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

print ("4.4 Structure from Known Poses (robust triangulation)")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.json", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
pRecons.wait()

print ("4.5 Export to PMVS")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2PMVS"),  "-i", reconstruction_dir+"/sfm_data.json", "-o", reconstruction_dir] )
print ("Der PMVS Ordner wurde aus der Datei "+reconstruction_dir+"/sfm_data.json in das Verzeichnis "+reconstruction_dir+" erstellt")
pRecons.wait()

print ("4.6. Export to CMPMVS")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2CMPMVS"),  "-i", reconstruction_dir+"/sfm_data.json", "-o", reconstruction_dir] )
print ("Der CMPMVS Ordner wurde aus der Datei "+reconstruction_dir+"/sfm_data.json in das Verzeichnis "+reconstruction_dir+" erstellt")
pRecons.wait()

print ("Workflow beendet")

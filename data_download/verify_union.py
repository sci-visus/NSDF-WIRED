# Ensure that we have copied all files in stop_gaps and union_set into final_union_set
import os

parent_dir = "/opt/wired-data/firesmoke"

# these subdirectories contain separate subsets of firesmoke netCDF files downloaded at separate times
# the union of these sets is all available files from firesmoke.ca from approx. Feb 2021 to present day (as of 11/12/2025)
subdirs = [
    "stop_gap_combined/stop_gapBSC00CA12-05",
    "stop_gap_combined/stop_gapBSC06CA12-05",
    "stop_gap_combined/stop_gapBSC12CA12-05",
    "stop_gap_combined/stop_gapBSC18CA12-05",
    "union_set",
    "hourly_downloads/data",
]

# directory to store union of all files in dirs above
final_union_set_dir = f"{parent_dir}/final_union_set"

# get list of files currently in final_union_set_dir
final_union_set_files = sorted(os.listdir(final_union_set_dir))

# to store any files not in final_union_set dir but is in subdir
missing_files = {
    subdir: [] for subdir in subdirs
}

# populate missing_files dict
for subdir in subdirs:
    files = sorted(os.listdir(f"{parent_dir}/{subdir}"))
    for file in files:
        if file not in final_union_set_files:
            missing_files[subdir].append(file)

# print results
for subdir, files in missing_files.items():
    print(f"Number of missing files: {len(files)}")
    print(f"{subdir}: {files}")
    print("---")

# # copy files not in final_union_set, into final_union_set
# for subdir, files in missing_files.items():
#     for file in files:
#         curr_dir_file = f"{parent_dir}/{subdir}/{file}"
#         save_dir_file = f"{final_union_set_dir}/{file}"
#         # copy file to final_union_set_dir
#         if not os.path.exists(save_dir_file):
#             with open(curr_dir_file, "rb") as curr_file:
#                 with open(save_dir_file, "wb") as save_file:
#                     save_file.write(curr_file.read())
#             print(f"Copied {curr_dir_file} -> {save_dir_file}")
#         else:
#             print(f"Skipping {curr_dir_file}; {save_dir_file} already exists.")
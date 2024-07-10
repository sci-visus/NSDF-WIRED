# ref: https://stackoverflow.com/questions/73678537/how-to-stack-videos-vertically-in-moviepy
from moviepy.editor import VideoFileClip, clips_array

# load netcdf and idx videos
netcdf_vid = VideoFileClip(
    "/usr/sci/scratch_nvme/arleth/dump/videos/netcdf_video_7_10_24.mp4", audio=False
)
idx_vid = VideoFileClip("/usr/sci/scratch_nvme/arleth/dump2/videos/idx_video_7_10_24.mp4", audio=False)

# stack the clips vertically
final_clip = clips_array([[netcdf_vid], [idx_vid]])

# Write the final video to a file using ffmpeg
final_clip.write_videofile("/usr/sci/scratch_nvme/arleth/dump2/videos/new_stack.mp4", codec="libx264", fps=netcdf_vid.fps)
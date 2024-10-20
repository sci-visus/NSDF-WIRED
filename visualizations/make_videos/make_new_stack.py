# ref: https://stackoverflow.com/questions/73678537/how-to-stack-videos-vertically-in-moviepy
from moviepy.editor import VideoFileClip, clips_array

# load netcdf and idx videos
vid1 = VideoFileClip(
    "/usr/sci/scratch_nvme/arleth/dump/videos/netcdf_parallel.mp4", audio=False
)
vid2 = VideoFileClip("/usr/sci/scratch_nvme/arleth/dump/videos/netcdf_serial.mp4", audio=False)

# stack the clips vertically
final_clip = clips_array([[vid1], [vid2]])

# Write the final video to a file using ffmpeg
final_clip.write_videofile("/usr/sci/scratch_nvme/arleth/dump/videos/netcdf_stack.mp4", codec="libx264", fps=vid1.fps)
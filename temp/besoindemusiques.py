# import os
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# video_file = "playlist for silly goofsters.webm"

# timestamps = [
#     ("0:00", "4:15", "pineapple_rag_techno_remake"),
#     ("4:15", "5:40", "scheming_weasel"),
#     ("5:40", "7:12", "kk_parade"),
#     ("7:12", "7:34", "spooktune"),
#     ("7:34", "9:15", "dokeshi_no_koshin"),
#     ("9:15", "15:12", "jades_theme"),
#     ("15:12", "16:47", "spazzmatica_polka"),
#     ("16:47", "19:22", "14_crush"),
#     ("19:22", "20:03", "tem_shop"),
#     ("20:03", "22:13", "drinky_bird"),
#     ("22:13", "23:26", "aquatic_race"),
#     ("23:26", "26:45", "pixel_peeker_polka"),
#     ("26:45", "27:26", "vs_lancer"),
#     ("27:26", "30:00", "pppp_papipupepo")
# ]

# output_folder = "output_folder"
# os.makedirs(output_folder, exist_ok=True)

# for i, (start_time, end_time, name) in enumerate(timestamps):
#     start_seconds = sum(x * int(t) for x, t in zip([60, 1], start_time.split(":")))
#     end_seconds = sum(x * int(t) for x, t in zip([60, 1], end_time.split(":")))
#     output_file = f"{output_folder}/{i}.webm"
    
#     ffmpeg_extract_subclip(video_file, start_seconds, end_seconds, targetname=output_file)


# ffmpeg -i 6.webm -vn 6.mp3

for i in range (7, 14):
    print('ffmpeg -i ', i,'.webm -vn ',i,'.mp3', sep='')
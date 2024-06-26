import os
import subprocess
import shutil
import sys

def split_large_video(video_path):
    # Kiểm tra kích thước tệp
    file_size = os.path.getsize(video_path)
    if file_size > 1 * 1024 * 1024 * 1024:  # 1GB
        # Tạo tên tệp cho các phần video
        part1_path = video_path.replace(".mp4", "_part1.mp4")
        part2_path = video_path.replace(".mp4", "_part2.mp4")
        
        # Cắt video ra làm 2 phần
        duration = subprocess.check_output(f"ffmpeg -i \"{video_path}\" 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//", shell=True).decode("utf-8").strip()
        h, m, s = duration.split(":")
        total_seconds = int(h) * 3600 + int(m) * 60 + float(s)
        half_duration = total_seconds / 2

        # Cắt phần 1
        subprocess.run(f"ffmpeg -i \"{video_path}\" -t {half_duration} -c copy \"{part1_path}\"", shell=True, check=True)
        # Cắt phần 2
        subprocess.run(f"ffmpeg -i \"{video_path}\" -ss {half_duration} -c copy \"{part2_path}\"", shell=True, check=True)

        # Xóa video gốc
        os.remove(video_path)

        return [part1_path, part2_path]
    return [video_path]

def process_video(video_path, output_dir, final_output_dir):
    print(f"Processing video: {video_path}")
    # Tách âm thanh bằng demucs
    command = f"python -m demucs.separate --out {output_dir} \"{video_path}\""
    subprocess.run(command, shell=True, check=True)

    # Đường dẫn tới tệp âm thanh giọng hát đã tách
    vocals_path = os.path.join(output_dir, "htdemucs", os.path.basename(video_path).replace(".mp4", ""), "vocals.wav")

    # Đường dẫn tới video tạm thời không có âm thanh
    temp_video_path = f"{video_path[0:-4]}_temp.mp4"

    # Tách âm thanh khỏi video và lưu lại video không có âm thanh
    subprocess.run(f"ffmpeg -i \"{video_path}\" -c copy -an \"{temp_video_path}\"", shell=True, check=True)

    # Thay âm thanh của video bằng âm thanh giọng hát đã tách và lưu video mới
    output_video_path = f"{video_path[0:-4]}_without_music.mp4"
    subprocess.run(f"ffmpeg -i \"{temp_video_path}\" -i \"{vocals_path}\" -c:v copy -c:a aac -strict experimental \"{output_video_path}\"", shell=True, check=True)

    # Kiểm tra nếu video_path chứa "without music"
    if "without music" in video_path:
        temp_dir = os.path.join(final_output_dir, "temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        shutil.move(temp_video_path, temp_dir)
    else:
        os.remove(temp_video_path)

    # Di chuyển video đã xử lý vào thư mục cuối cùng
    final_video_path = os.path.join(final_output_dir, os.path.basename(video_path).replace(".mp4", "_without_music.mp4"))
    shutil.move(output_video_path, final_video_path)

    # Xóa video gốc
    os.remove(video_path)

if __name__ == "__main__":
    output_directory = "demucs_output"  # Thư mục lưu kết quả xử lý
    final_output_directory = "videos_without_music"  # Thư mục chứa video sau khi xử lý
    input_dir = "videos"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if not os.path.exists(final_output_directory):
        os.makedirs(final_output_directory)
      
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".mp4"):
            video_path = os.path.join(input_dir, file_name)
            video_parts = split_large_video(video_path)
            for part in video_parts:
                process_video(part, output_directory, final_output_directory)

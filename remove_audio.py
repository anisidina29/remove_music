import os
import subprocess
import threading
import shutil

def process_video(video_path, output_dir, final_output_dir):
    print(video_path)
    # Tách âm thanh bằng demucs
    command = f"python -m demucs.separate -d cuda --out {output_dir} {video_path}"
    subprocess.run(command, shell=True)

    # Đường dẫn tới tệp âm thanh giọng hát đã tách
    vocals_path = os.path.join(output_dir, "htdemucs", os.path.basename(video_path).replace(".mp4", ""), "vocals.wav")

    # Đường dẫn tới video tạm thời không có âm thanh
    temp_video_path = f"{video_path[0:-4]}_temp.mp4"

    # Tách âm thanh khỏi video và lưu lại video không có âm thanh
    subprocess.run(f"ffmpeg -i {video_path} -c copy -an {temp_video_path}", shell=True)

    # Thay âm thanh của video bằng âm thanh giọng hát đã tách và lưu video mới
    output_video_path = f"{video_path[0:-4]}_without_music.mp4"
    subprocess.run(f"ffmpeg -i {temp_video_path} -i {vocals_path} -c:v copy -c:a aac -strict experimental {output_video_path}", shell=True)

    # Di chuyển video đã xử lý vào thư mục cuối cùng
    final_video_path = os.path.join(final_output_dir, os.path.basename(video_path).replace(".mp4", "_without_music.mp4"))
    shutil.move(output_video_path, final_video_path)

    # Xóa video tạm thời
    os.remove(temp_video_path)
    os.remove(video_path)
def process_all_videos(input_dir, output_dir, final_output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(final_output_dir):
        os.makedirs(final_output_dir)

    threads = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".mp4"):
            video_path = os.path.join(input_dir, file_name)
            thread = threading.Thread(target=process_video, args=(video_path, output_dir, final_output_dir))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    input_directory = "videos"  # Thư mục chứa các video gốc
    output_directory = "demucs_output"  # Thư mục lưu kết quả xử lý
    final_output_directory = "videos_without_music"  # Thư mục chứa video sau khi xử lý

    process_all_videos(input_directory, output_directory, final_output_directory)

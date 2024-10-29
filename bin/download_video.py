import yt_dlp

def download_facebook_video(url, output_path):
    ydl_opts = {
        'outtmpl': output_path,  # Path where the downloaded file will be stored
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Ensures best quality video and audio
        'merge_output_format': 'mp4',  # Merges into mp4 format
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # Convert video to mp4 format
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example usage
facebook_video_url = 'https://www.facebook.com/senamhiperu/videos/jueves-cientifico/798966251677644'
output_path = 'quispe_video2.mp4'
download_facebook_video(facebook_video_url, output_path)
print(f'Video downloaded to {output_path}')

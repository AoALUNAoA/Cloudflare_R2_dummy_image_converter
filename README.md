![Build Status](https://github.com/AoALUNAoA/Cloudflare_R2_dummy_image_converter/actions/workflows/python-app.yml/badge.svg)

# Cloudflare_R2_dummy_image_converter
My dummy tool allows you to automatically batch process images in your bucket, from a specified timestamp up to the latest timestamp of images uploaded to that bucket, rather than entire bucket images. You simply select the source image path, the destination image path, and enter the target timestamp.<br><br>
Once you've stored a lot of images in your Cloudflare R2 bucket, you might need to convert some images within a specific timeframe to a designated format in some cases, rather than converting the entire bucket. This can present some challenges.


## 1.ENV
```python
python3 -m venv .venv
source .venv/bin/activate
pip install requests boto3 pillow
```

## 2.Enter filepath and target image timestamp

```python
python3 Cloudflare_R2_dummy_image_converter.py
```
After running the script, you'll be prompted to enter input&output path and target timestamp in the command line. You could obtain this information from your Cloudflare R2 bucket's folder path and the timestamp of your desired target images.<br>
You could get something like this:
```shell
Please enter the path to the images in CF bucket you want to process: posters/
Please enter the destination folder path for the converted images: posters/
Provide the starting timestamp in the following exactly format: YYYY-MM-DD HH:MM:SS: 2025-03-03 02:57:26
Uploaded Successfully: posters/poster_245891.webp
Successfully Done!: posters/poster_245891.jpg -> posters/poster_245891.webp
Uploaded Successfully: posters/poster_11527.webp
Successfully Done!: posters/poster_11527.jpg -> posters/poster_11527.webp
.
.
.
```
## 3.Frontend
```html
<picture>
    <source srcset="https://your_Cloudflare_R2_bucket_domain.com/posters/poster_245891.webp" type="image/webp" />
    <source srcset="https://your_Cloudflare_R2_bucket_domain.com/posters/poster_245891.jpg" type="image/jpeg" />
    <img class="poster" src="https://your_Cloudflare_R2_bucket_domain.com/poster_245891.jpg" alt="photo" />
</picture>
```
You could display the same image data in two different formats on your website's front end, thus reducing bandwidth requirements for most devices accessing image-heavy websites and improving your Google PageSpeed score.

## Note
I am a dedicated patent agent. This code is a personal project and is not guaranteed to be suitable for production environments. Use at your own risk.

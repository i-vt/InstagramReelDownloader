# InstagramReelDownloader

##  Build the image
`docker build -t instagram-scraper .`
## Run it
`docker run -p 5000:5000 --name igscraper instagram-scraper`

## Remove
Also to troubleshoot, you can remove the container and then re-run it `docker rm igscraper` 

## Optimizing
If you feel lucky, you can reduce lag by lowering the values: `time.sleep(random.randint(2000, 4000) / 100)`, specifically the `2000` and the `4000`

## GUI Preview
(Reel URL goes into the textbox under the "Instagram Post URL:" label)
### Desktop
![image](https://github.com/user-attachments/assets/e00871de-96fc-4b3a-9398-0b7866c8d46f)

### Phone
![image](https://github.com/user-attachments/assets/a4b15495-9971-4b2b-bebb-11ff5e908938)

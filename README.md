# Emojisaic

In order to create your own mosaic-making web site, firstly check that you have got all the dependencies and follow the steps in the ipython notebook to create your color-image lookup table

## API 

Just send a simple GET request to http://www.emojisaic.com/api?url=YOUR_URL_TO_IMAGE

The server will return a JSON dictionary containing only one key, "public_url", pointing to the public S3 URL of the emojifyed picture

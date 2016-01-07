## Google Image Search (only Face type)

```
usage: google_image_search.py [-h] [-c COUNT] [-o OUTPUT] [--no-header]
                              [-r RETRY]
                              input

Google Image Search (Face type)

positional arguments:
  input                 Input file name

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number of image per name
  -o OUTPUT, --output OUTPUT
                        Output CSV file name
  --no-header           Output without header at the first row
  -r RETRY, --retry RETRY
                        Number of retry if errors
```

### Example

```
python google_image_search.py output.csv
```

Default output file will be save as `output-img.csv`. There are two columns added by the script.

* `image_url` - URL link to the image
* `image_order` - Order of image in search results
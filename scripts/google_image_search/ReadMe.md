## Google Image Search (only Face type)

The script takes a csv with first names ([sample input file](sample_in.csv)), searches for images and returns links to the image. In particular, the script appends the following two columns: 

* `image_url` - URL link to the image
* `image_order` - Order of image in search results

### Installation

To begin using the script, first install the [requirements](../requirements.txt). Then run the downloaded script.

### Usage

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
python google_image_search.py sample_in.csv
```


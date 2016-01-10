## Get image tags from Clarifai

[Clarifai](http://clarifai.com) for now only tags ".jpg", ".jpeg" and ".png" images. So limit yourself to those images. 

To begin, install the [requirements](../requirements.txt). In particular, the script depends on pandas and [clarifai API client](https://github.com/Clarifai/clarifai-python).

Before running the script, please set `app_id` and `app_secret` in [`clarifai.cfg`](clarifai.cfg) or make sure the environment variables `CLARIFAI_APP_ID` and `CLARIFAI_APP_SECRET` are set.

```
usage: clarifai_tag.py [-h] [--config CONFIG] [-c COUNT] [-b BATCH]
                       [-o OUTPUT] [--no-header]
                       input

Clarifai Tag API

positional arguments:\github\clarifai_gender\dev\scripts\get_clarifai_tags
  input                 Input file name

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  -c COUNT, --count COUNT
                        Number of valid tag for each item
  -b BATCH, --batch BATCH
                        Specify batch size
  -o OUTPUT, --output OUTPUT
                        Output CSV file name
  --no-header           Output without header at the first row
```

### Example

To get at least 20 tags per image:

```
python clarifai_tag.py sample_in.csv -c 20 
```

Default name of the output file is `output-img-tag.csv`. The script appends the following new columns:

* `clarifai_status`:
    * None: URLs haven't tagged by Clarifai (include URLs was filtered out)  
    * OK: Tagged by Clarifai with OK status  
    * ALL_ERROR => Failed to tag by Clarifai, if there is video URL in the batch.  
    * CLIENT_ERROR => Failed to tag by Clarifai  
    * ERROR => if there is Error in the script

    In case the status is "ALL_ERROR", we can reset these errors manually (just delete the status) and re-run the script with a smaller batch size. (-b option in `clarify_tag.py`)

* `tags`: Tags returned by clarifai
* `probs`: Probability of each tag being applicable, returned by clarifai
* `predicted`: Predicted gender for the person(s) in the image
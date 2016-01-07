## Stratified random sample

The script is used only during validation.
```
usage: sample_input.py [-h] [-o OUTPUT] [-c COUNT] [-m MIN_LEN] [-t TYPE]
                       [--no-header]
                       input

Stratified random sample male/female first name

positional arguments:
  input                 Input file name

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output CSV file name
  -c COUNT, --count COUNT
                        Number of name to sample
  -m MIN_LEN, --min-len MIN_LEN
                        Mininum name length
  -t TYPE, --type TYPE  Politician Type (all, state, local)
  --no-header           Output without header at the first row
```

#### Example

Run the script to output 100 stratified random sample male/female first names. (50/50 men/women)

```
python sample_input.py -c 100 -t state data/india-mps-all-gender.csv.bz2

```

Default output file will be `output.csv`
# Code to generate a minimised set of web form constraints for GLAMOD

This code can take in a space-delimited text file of structure:

```
header
record
record
record
```

It will iterate over the contents to group the records into a minimal
list of dictionaries of constraints. The constraints can then be used 
in the forms in the CDS web-interface.

## Usage

```
python3 minimise-constraints.py <input_file>
```

E.g.:

```
python3.6 minimise-constraints.py counts.land
```

This writes: `constraints.json`

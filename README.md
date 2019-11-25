# ZwoReader
Code for reading a zwo file. The zwo file format is an XML-based format that describes a workout.

## Using
```python
reader = ZwoReader()
reader.read_file("foo.zwo")
for interval in reader.workout:
    print(interval)
```

### Option 1
Add the source files (Zwo*.py) directly to your project.

### Option 2
Via PIP (I haven't set this up yet)

## Version History

## License
This library is released under the MIT license, see LICENSE for details.

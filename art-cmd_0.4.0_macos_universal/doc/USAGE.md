# Usage examples of the ARRI Reference Tool (commandline version)

Examples are based on the following filetree of input clips

```
[C:]/
└── path/
    └── clips/
        ├── filename.mxf
        └── ari_dirname/
            ├── ari_filename06.ari    // "--start 0" ─┐
            ├── ari_filename07.ari                   ─┤
            ├── ari_filename08.ari                   ─┘ "--duration 3" (from start = 0)
            ├── ari_filename09.ari    // "--start 3" ─┐
            ├── ari_filename10.ari                   ─┘ "--duration 2" (from start = 3)
            ├── ari_filename11.ari    // "--start 5"
            └── ...
```

<br/>

## 'process' mode

### to .exr in ACES 'AP0/D60/linear' colorspace (default) or 'AWG[3/4]/D65/linear'

By default

`art-cmd process --input /path/clips/filename.mxf`

renders files in ACES 'AP0/D60/linear' colorspace in the following structure

```
./process/
  └── filename/
      ├── 0000000.exr
      ├── 0000001.exr
      ├── 0000002.exr
      └── ...
```

given the input structure on top.

<br/>

Explicitly stating an output path pattern, e.g.

`art-cmd process --input /path/clips/filename.mxf --output aces_ap0/frame%06d.exr`

renders

```
./aces_ap0/
  ├── frame000001.exr
  ├── frame000002.exr
  ├── frame000003.exr
  └── ...
```

<br/>

For rendering to 'AWG[3/4]/D65/linear' instead of ACES 'AP0/D60/linear', the target colorspace argument must be added, e.g.

`art-cmd process --input /path/clips/filename.mxf --target-colorspace 'AWG4/D65/linear' --output awg4/frame%06d.exr`

renders

```
./awg4/
  ├── frame000001.exr
  ├── frame000002.exr
  ├── frame000003.exr
  └── ...
```

*Note*: Compression of the written exr-files can be achieved by adding a corresponding video codec as argument for writing .exr files, like e.g. 
"--video-codec 'exr_piz/f16'". The default is 'exr_uncompressed/f16'.

<br/>

### to .tif in LogC[3/4] or display colorspace

For rendering to .tif in 'AWG3/D65/LogC3' (default for footage from ALEXA Mini LF or older cameras) or LogC4 colorspace (default for from ALEXA 35 or 
newer cameras), an explicit output path-pattern ending with .tif must be stated, e.g.

`art-cmd process --input /path/clips/filename.mxf --output logc/%07d.tif`

rendering

```
./logc/
  ├── 0000000.tif
  ├── 0000001.tif
  ├── 0000002.tif
  └── ...
```

*Note*: Rendering to 'AWG4/D65/LogC4' colorspace is possible for all inputs by adding the "--target-colorspace 'AWG4/D65/LogC4'" argument.

<br/>

### batch processing

It is possible to state a directory containing several input clips which are then batch-processed to several output-clips, replicating the input
directories structure, e.g.

`art-cmd process --input /path/clips/ --start 2 --output batch/`

renders (given the input structure on top) to, by default, .exr files in ACES 'AP0/D60/linear' colorspace

```
./batch/
  ├── filename/
  │   ├── 0000002.exr
  │   ├── 0000003.exr
  │   └── ...
  └── ari_dirname/
      └── ari_filename/
          ├── 0000002.exr // from ari_filename08.ari
          ├── 0000003.exr // from ari_filename09.ari
          └── ...
```

<br/>

To render everything to .tif files in 'AWG4/D65/LogC4' colorspace, the call is e.g.

`art-cmd process --input /path/clips/ --target-colorspace 'AWG4/D65/LogC4' --output logc4_batch/frame%07d.tif`

that renders

```
./logc4_batch/
  ├── filename/
  │   ├── frame0000000.tif
  │   ├── frame0000001.tif
  │   └── ...
  └── ari_dirname/
      └── ari_filename/
          ├── frame0000000.tif // from ari_filename06.ari
          ├── frame0000001.tif // from ari_filename07.ari
          └── ...
```

*Note*: In following examples batch processing inputs will not be described separately as behavior is the same.

<br/>

## 'trim' mode (creating RDD54/55 conformant MXF files)

### cut clip

`art-cmd trim --input /path/clips/filename.mxf --start 180 --duration 12000`

renders

```
./trim/
  └── filename.mxf
```

containing frame 180 to 12180 of the uncut clip.

*Note*: Setting '--start' and '--duration' is always possible to just feed a cut of an input clip into the tool.

<br/>

### rewrap clip

#### ari/arx inputs

`art-cmd trim --input /path/clips/ari_dirname/`

renders

```
./trim/
  └── ari_filename.mxf
```

containing all ari/arx frames from the *ari_dirname* directory, where files must be named according to the pattern
*[ari_filename][counter-with-leading-zeroes].ari*

*Note*: In following examples ari/arx inputs will not be described separately as behavior is the same.

<br/>

#### mxf inputs

##### to current directory
`art-cmd trim --input /path/clips/filename.mxf`

renders

```
./trim/
  └── filename.mxf
```

which is a new directory "trim/filename.mxf" created in the current
directory (e.g. *2024-06-25_15-29-54-978+0200_trim/filename.mxf*)

<br/>

##### to custom output directory

`art-cmd trim --input /path/clips/filename.mxf --output out/`

renders

```
./out/
  └── filename.mxf
```

while creating all missing directories.

<br/>

##### to custom output filepath

`art-cmd trim --input /path/clips/filename.mxf --output /path/trim.mxf`

renders the new mxf file to the explicitly specified output path and creates all
missing directories

*Note*: In following examples "--output" will be omitted when the behavior is
the same as described here.

<br/>

#### multiple inputs

`art-cmd trim --input "/path/clips/filename.mxf","/path/clips/ari_dirname/"`

or

`art-cmd trim --input /path/clips/filename.mxf --input /path/clips/ari_dirname/`

renders

```
./trim/
  ├── filename.mxf
  └── ari_dirname
      └── ari_filename.mxf
```

Note: In following examples multiple inputs will not be described separately as behavior is the same.

<br/>

## 'export' mode

### export audio

`art-cmd export --input /path/clips/filename.mxf --output mono_audio_track.wav --duration 2`

renders (for mxf containing two mono audio tracks)

```
./
├── mono_audio_track00.wav
└── mono_audio_track01.wav
```

<br/>

### export metadata

`art-cmd export --input /path/clips/filename.mxf --output metadata_export.json`

renders all metadata (static clip- dynamic frame-metadata) into

```
./
└── metadata_export.json
```

<br/>

### export audio and metadata to directory

`art-cmd export --input /path/clips/filename.mxf --output export_dir/`

exports all audio and metadata (static clip- dynamic frame-metadata) to

```
./export_dir/
  ├── audio_track00.wav
  ├── audio_track01.wav
  └── metadata.json
```

*Note*: The arguments '--skip-metadata' and '--skip-audio' can also be used to skip a certain part of the export.

<br/>

## 'verify' mode

### one clip (recalculating checksums for video-frames and checking against metadata)

`art-cmd verify --input /path/clips/filename.mxf` or

`art-cmd verify --input /path/clips/ari_dirname/`

will print all recalculated video-checksums that do not match as human-readable messages to the log as errors.

<br/>

### two clips (comparing video-checksums, audio- and video-data)

`art-cmd verify --input /path/clips/filename.mxf --input /path/trim/filename.mxf`

will verify that the rewrap [to custom output filepath](#to-custom-output-filepath) from the first example on top contains the same data as the original clip,
while printing all video-checksum, audio- or metadata differences to `./art.log` as error.

<br/>
# ARRI Reference Tool (commandline version)

## [0.4.0] - 2025-07-18

### Added

- [IS-8902] Added support for reading MXF/ProRes files and apply some look transformation (if in LogC colorspace).
- [IS-8866] Added possibility to parameterize processing from JSON files, that may contain parameters for both ARRIRAW and ARRICORE processing.
- [IS-8866] Added support for processing ARRICORE essence containers.
- [IS-8670] Added support for MXF/ProRes rendering output (option --video-codec=prores*). 
- [IS-8401] Added support for ARRICORE essence container.
- [IS-8836] Added '--verbose' option to specify the level of verbosity and extended logging with info about progress of batch.

### Fixed

- [IS-8650] Fixed incorrect read out and conversion of Lens Converter values for legacy clips.
- [IS-8668] Fixed unknown MXF labels containing LUT keys.
- [IS-8733] Fixed unknown MXF labels containing deprecated Image Processing Model Parameter Table keys.
- [IS-8813] Fixed unknown MXF labels containing deprecated Video Codec Version key.
- [IS-8805] Fixed unknown MXF labels containing Described Track IDs key.
- [IS-8674] Fixed Instance UID being the same for multiple MXF Identification Sets.

## [0.3.2] - 2025-03-18

### Fixed

- [BUG-9534] Fixed regex error with '--cli' option on macOS.
- [IS-none] Fixed not exiting with error result when a single explicitely stated input clip cannot be read.

### Added

- [IS-8605] Added support for clip recovery of not finalized MXF clips with mode 'mxf-recovery'.

### Changed

- [IS-8600] When unknown MXF labels are present in a clip provided for 'export' mode, execution will fail,
  producing an error telling to update the software. In other modes, a warning will be logged in this case.

## [0.3.1] - 2025-02-03

### Added

- [IS-8549] Added the commandline argument '--logpath' to specify a path for the log file.

### Fixed

- [IS-8549] Fixed aborting program execution when logpath was not writable, now continuing without writing log to file in this case.


## [0.3.0] - 2025-01-17

### Added


- [IS-8126] Added 'export' mode for extracting metadata to JSON and audio to WAV.

- [IS-8323] Added ability to render files with letterboxed frames using black bars (e.g. TIF) or via metadata (e.g.
  OpenEXR) via recipe argument '--letterbox-size'.
- [IS-8402] Added rendering support for monochrome ALEXA35 and ALEXA265 clips.
- [IS-8410] Added support for rendering 32bit OpenEXR files.

### Fixed

- [IS-8438] Fixed out-folder structure when processing batches (directories were missing or duplicated) and output file
            numbering, which now always start from filename '0' (or '--start' number if given as argument).
- [IS-8333] Fixed misleading warnings and false errors while reading MXF clips.


## [0.2.3] - 2024-10-14

### Fixed


- [IS-8311] When batch processing multiple input clips, a subfolder for each input clip will be created.
- [IS-8294] Consider parameter `--video-codec` for OpenExr compression method.


## [0.2.2] - 2024-09-13

### Added

- [IS-8116] Implemented functionality for the following command line arguments:
  `mode process, --processing-mode, --processing-device, --ls-devices, --embedded-look, --target-colorspace, --ls-target-colorspaces`.
  This basically enables the art-cmd to render arriraw clips into OpenExr and TIF output format.


## [0.2.1] - 2024-08-29

### Changed

- [IS-7954] Changed structure generated when batch processing multiple inputs to an output folder, which had the filename
  duplicated when input was %07d.ari and generated *ari_filename*%07d.mxf which is now just *ari_filename*.mxf.
- [IS-7954] Default output folder is now just the mode, which is deterministic in contrast to the timestamps used before.
  If the output folder already exists and is not empty, processing into it will be skipped to not overwrite existing MXF files.
  The current directory as output argument is now explicitly forbidden so source files cannot
  be overwritten while being read.


## [0.1.2] - 2024-07-05

### Fixed

- [IS-8096] Fixed wrong handling of duration argument in trim mode.


## [0.1.1] - 2024-07-04

### Added

- [IS-7993] Implemented support for batch processing all clips from an input folder to an output folder.
- [IS-7855] Implemented *trim* mode functionality.
- [IS-7896] Implemented *verify* mode functionality.
- [IS-7657] Initial artcmd application and schema as json, --help text generation from schema and --version.
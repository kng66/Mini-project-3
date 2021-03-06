# Mini-project-3

## Info
This repository consists of the parse file. The pydicom package is to read DICOM file and transfer DICOM tags into a dictionary. The dictionary will recevice information of the DICOM image file and parsed into a FHIR ImagingStudy resourse standard.

### Installation

This application requires Python 3 to run.

Dependencies:

* pydicom
* json
* copy

Dependencies can be installed via `pip` command, for example:

```sh
$ pip install pydicom
``` 

The dataset can be found here: https://github.com/ImagingInformatics/hackathon-dataset

### Usage

The DICOM processor requires a path to the study folder, which should contain other folders and files grouped as follows:
```sh
   |- Patients
      |- study
         |- Series
             |- Instances (.dcm files)
```

### Templating

The parsing uses pydicom function to_json_dict() to access each DICOM tag as a key and DICOM metadata as the value.  

Currently, the Integration engine comes with one templates:
- template for `ImagingStudy` FHIR objects (integrating DICOM image metadata with FHIR HL7-based servers),


### Example

```sh
$ python main.py -i ./StudyFolder -o output.txt
```

import os
import pydicom
import json
import copy

# hackathon-dataset/hackathon-images/Sally-SIIM/Digital_Diagnostic_Mammogram_Bilateral - 0/L_CC_3/IM-0007-0012.dcm


class Config:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def render_template(self):
        directory = ''
        for base, dirs, files in os.walk(self.root_dir):
            if files:
                directory = base
                break

        first_files_name = os.listdir(f'{directory}/')[0]

        with open(f'{directory}/{first_files_name}', 'rb') as infile:
            ds1 = pydicom.dcmread(infile)

        ds1 = ds1.to_json_dict()
        del ds1['7FE00010']

        imagingstudy = {}
        imagingstudy['resourceType'] = 'ImagingStudy'
        imagingstudy['id'] = ds1['00080050']['Value'][0]
        imagingstudy['test'] = {}
        imagingstudy['test']['status'] = 'generated'
        imagingstudy['test']['div'] = '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + \
            ds1['00081030']['Value'][0] + '</div>'
        imagingstudy['identifier'] = []

        sys_section = {}
        sys_section['system'] = 'urn:dicom:uid'
        sys_section['Value'] = 'urn:oid:' + ds1['0020000D']['Value'][0]
        imagingstudy['identifier'].append(sys_section)

        usage = {}
        usage['use'] = 'usual'
        usage['type'] = {}
        usage['type']['coding'] = []
        coding = {}
        coding['system'] = 'http://terminology.hl7.org/CodeSystem/v2-0203'
        coding['code'] = 'ACSN'
        usage['type']['coding'].append(coding)
        usage['value'] = ds1['00080050']['Value'][0]
        usage['assigner'] = {'reference': 'Organization/siim'}
        imagingstudy['identifier'].append(usage)

        patient_name = ds1['00100010']['Value'][0]["Alphabetic"].lower()
        patient_name = ''.join(char for char in patient_name if char.isalnum())

        imagingstudy['subject'] = {'reference': 'Patient/' + patient_name}

        date = ds1['00080020']['Value'][0]
        imagingstudy['started'] = date[:4] + '-'+date[4:6] + '-' + date[6:8]

        imagingstudy['endpoint'] = []
        end_reference = {'reference': 'Endpoint/siim-dicomweb'}
        imagingstudy['endpoint'].append(end_reference)

        app_folder = self.root_dir + '/'
        totalFiles = 0
        totalDir = 0

        for base, dirs, files in os.walk(app_folder):
            for directories in dirs:
                totalDir += 1
            for Files in files:
                totalFiles += 1

        imagingstudy['numberOfSeries'] = totalDir
        imagingstudy['numberInstances'] = totalFiles
        imagingstudy['description'] = ds1['00081030']['Value'][0]

        imagingstudy['series'] = []

        series = []
        series_section = {}
        instance_section = {}
        for base, dirs, files in os.walk(app_folder):
            numberOfInstance = 0
            instance = []
            for file in files:
                with open(f'{base}/{file}', 'rb') as infile:
                    ds = pydicom.dcmread(infile)
                ds = ds.to_json_dict()
                del ds['7FE00010']
                new_instance_section = copy.deepcopy(instance_section)
                new_instance_section['number'] = ds['00200013']['Value'][0]
                new_instance_section['uid'] = 'urn:oid:' + \
                    ds['00080018']['Value'][0]
                new_instance_section['sopClass'] = ds['00080016']['Value'][0]
                instance.append(new_instance_section)
                numberOfInstance += 1
            if files:
                new_series_section = copy.deepcopy(series_section)
                new_series_section["number"] = ds['00200011']['Value'][0]
                new_series_section['modality'] = {
                    "system": "http://dicom.nema.org/resources/ontology/DCM", "code": ds['00080060']['Value'][0]}
                new_series_section['uid'] = 'urn:oid:' + \
                    ds['0020000E']['Value'][0]
                new_series_section['description'] = ds['0008103E']['Value'][0]
                new_series_section['numberOfInstances'] = numberOfInstance
                new_series_section['instance'] = instance
                series.append(new_series_section)

        imagingstudy['series'] = series

        return imagingstudy

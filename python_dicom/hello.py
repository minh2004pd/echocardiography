import os
import orthanc
import json
import pprint
# from DicomManager import DicomManager



def OnStoredInstance(dicom, instanceId):
    print('Received instance %s of size %d (transfer syntax %s, SOP class UID %s)' % (
        instanceId, dicom.GetInstanceSize(),
        dicom.GetInstanceMetadata('TransferSyntax'),
        dicom.GetInstanceMetadata('SopClassUid')))

    # Print the origin information
    if dicom.GetInstanceOrigin() == orthanc.InstanceOrigin.DICOM_PROTOCOL:
        print('This instance was received through the DICOM protocol')
    elif dicom.GetInstanceOrigin() == orthanc.InstanceOrigin.REST_API:
        print('This instance was received through the REST API')
    
    print(instanceId)
    print("helloabc")

    # Write the instanceId to a file in the Docker volume
    with open('/etc/orthanc/instance_ids.txt', 'w') as f:
        f.write(instanceId + '\n')

    
orthanc.RegisterOnStoredInstanceCallback(OnStoredInstance)
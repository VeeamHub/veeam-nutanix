# Run under any backup administrator account

Import-Module '.\VeeamNutanixUnofficialV5'

#
# Skip SSL errors. We work with localhost only here, so not that critical.
# You may want to get thumbprint and specify it for a request for the security reasons.
#
add-type @"
using System.Net;
using System.Security.Cryptography.X509Certificates;
public class TrustAllCertsPolicy : ICertificatePolicy {
    public bool CheckValidationResult(
        ServicePoint srvPoint, X509Certificate certificate,
        WebRequest request, int certificateProblem) {
        return true;
    }
}
"@
$AllProtocols = [System.Net.SecurityProtocolType]'Ssl3,Tls,Tls11,Tls12'
[System.Net.ServicePointManager]::SecurityProtocol = $AllProtocols
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy


#
# Get parameters for Instant Recovery
#

# For the test -- take the first cluster
$clusters = [array](Get-NutanixClusters)
$clusterUuid = $clusters[0].id

# For the test -- take the first network
$networks = Get-NutanixClusterNetworks -clusterUuid $clusterUuid
$networkUuid = $networks[0].uuid
#Get-NutanixClusterNetwork -clusterUuid $clusterUuid -networkUuid $networkUuid 

# For the test -- get first container
$containers = Get-NutanixClusterStorageContainers -clusterUuid $clusterUuid
$containerUuid = $containers[0].containerUuid


# For the test - take the first backup, take the last point from it, take OIB id from it
$nutanixParentBackups = Get-VBRBackup | Where-Object {$_.BackupPlatform.PlatformId.Guid -eq '799a5a3e-ae1e-4eaf-86eb-8a9acc2670e2'} #get all Nutanix backups
$childBackups = $nutanixParentBackups[0].FindChildBackups()
$point = $childBackups[0].GetLastPoint()
$oib = $point.GetOibs()[0]
$oibId = $oib.Id.Guid

# You can get the original VM metadata from a restore point here
$meta = Get-VbrVmMetadata -restorePointUuid $oibId


#
# Perform Instant Recovery
#

# Run publushing
$irSession = Publish-NutanixVm -clusterUuid $clusterUuid -containerUuid $containerUuid -networkUuid $networkUuid -namePrefix "sb-test-" -restorePointUuid $oibId -restoreReason "Test PowerShell"
WaitForIrMount -irSessionTag $irSession.sessionTag
#Get-NutanixIrSession -sessionTag $irSession.sessionTag


# Get VM details
$vbrSession = Get-VbrSessionByTag -sessionTag $irSession.sessionTag
$sessionMetadata = ($vbrSession.serializedData | ConvertFrom-Json)
$newVmId = $sessionMetadata.restoredVirtualMachineId
$newVm = Get-NutanixVM -clusterUuid $clusterUuid -vmUuid $newVmId
#Will get the first one if VM has multiple IPs
$newVmIpAddress = $newVm.ipAddress

#
# Here can be your code for VM testing
#

# ... (use $newVmIpAddress, $newVmId)


#
# Unpublish VM (stop Isntant Recovery)
#
$session = Unpublish-NutanixVm -sessionTag $irSession.sessionTag